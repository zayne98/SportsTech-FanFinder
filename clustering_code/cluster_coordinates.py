
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import folium
import random

# Todo: 
#   One value
#   No values
#   Duplicate values
# Currently supports at most 15 teams (15 potential colors to choose from. Can add more)

# --------------------------------------

# Supported folium color options
colors =  ['red', 'blue', 'green', 'purple', 'orange', 
    'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 
    'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen']

# --------------------------------------

# Load in the gps_data and add column headers

gps_data = pd.read_csv('gps_data.csv', header=None)
num_cols = gps_data.shape[1]
if (num_cols > 2): 
    gps_data.columns = ['latitude', 'longitude', 'team']
else:
    gps_data.columns = ['latitude', 'longitude']


# --------------------------------------

# Initialize unclustered map
unclustered_map_center = [gps_data['latitude'].mean(), gps_data['longitude'].mean()]
unclustered_map_zoom = 12
unclustered_map = folium.Map(location=unclustered_map_center, zoom_start=unclustered_map_zoom)


# Initialize cluster map
clustered_map_center = [gps_data['latitude'].mean(), gps_data['longitude'].mean()]
clustered_map_zoom = 12
clustered_map = folium.Map(location=clustered_map_center, zoom_start=clustered_map_zoom)

# --------------------------------------


def plot_one_team(gps_data_subset, color, team_label):
    # add points to the unclustered map
    for i, row in gps_data_subset.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            fill=True,
                            color=color,
                            fill_color=color,
                            fill_opacity=0.5,#).add_to(unclustered_map)
                            tooltip=team_label).add_to(unclustered_map)


    # find the optimal number of clusters to use for k-means
    coordinates = gps_data_subset[['latitude', 'longitude']].values
    X = np.array(coordinates)

    wcss = []
    for i in range(1, len(coordinates)+1):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)

    try:
        second_deriv = np.gradient(np.gradient(wcss))
        inflection_point = np.where(np.diff(np.sign(second_deriv)))[0][0]
        knee = inflection_point
    except:
        print(" *** EXCEPT ***")
        knee = 1

    # Cluster the GPS coordinates using the optimal number of clusters
    kmeans = KMeans(n_clusters=knee, init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_kmeans = kmeans.fit_predict(X)

    # --------------------------------------

    # Compute the weight associated with each cluster center
    weights = np.bincount(y_kmeans)

    weighted_gps_data = pd.DataFrame({'latitude': kmeans.cluster_centers_[:, 0],
                    'longitude': kmeans.cluster_centers_[:, 1],
                    'weight': weights})

    # weighted_gps_data.to_csv('weighted_gps_data.csv', index=False)

    # --------------------------------------


    # Create a map with the markers sized by the weight of each center point
    for i, row in weighted_gps_data.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=row['weight'] * 2, # CHANGE THIS WEIGHT
                            fill=True,
                            color=color,
                            fill_color=color,
                            fill_opacity=0.5,#).add_to(clustered_map)
                            tooltip=team_label).add_to(clustered_map)


# --------------------------------------


# Run clustering for each team

if (num_cols > 2):
    teams = set(gps_data['team'].unique())
    team_index = 0
    for team in teams:
        data_subset = gps_data[gps_data['team'] == team]
        plot_one_team(data_subset, colors[team_index], team)
        team_index += 1
else:
    plot_one_team(gps_data, colors[0], "Team")


unclustered_map.save('unclustered_unweighted_map.html')
clustered_map.save('weighted_map.html')
