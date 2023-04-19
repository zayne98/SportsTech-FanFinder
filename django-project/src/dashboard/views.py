from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Data
from .forms import AddLocationForm

from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import folium
import random
import geocoder


from django.http import HttpResponseRedirect

# Supported folium color options
colors =  ['red', 'blue', 'green', 'purple', 'orange', 
    'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 
    'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen']

# Create your views here.
def thanks(request):
    context = {}
    return render(request, 'dashboard/thanks.html', context)

def add_location(request):
    context = {}
    if request.method == "POST":
        form = AddLocationForm(request.POST)
        if form.is_valid():
            t_name = form.cleaned_data.get("team_name")
            lat = form.cleaned_data.get("latitude")
            long = form.cleaned_data.get("longitude")
            new_data = Data(team_name=t_name, latitude=lat, longitude=long)
            new_data.save()
            return HttpResponseRedirect("/thanks/")
    else:
        form = AddLocationForm()
        context['form'] = form
        return render(request, 'dashboard/add_location.html', context)
    

def increase_team_A(request):
    if (request.method == "POST"):
        t_name = "A"
        lat = 40.462325
        long = -80.031731

        new_data = Data(team_name=t_name, latitude=lat, longitude=long)
        new_data.save()

    return HttpResponseRedirect(reverse('map-clustered'))
    
def increase_team_B(request):
    if (request.method == "POST"):
        t_name = "B"
        lat = 40.460813
        long = -79.928361

        new_data = Data(team_name=t_name, latitude=lat, longitude=long)
        new_data.save()

    return HttpResponseRedirect(reverse('map-clustered'))

def submit_user_info(request):
    if (request.method == "POST"):
        location_string = request.POST.get("location-string")
        team_string = request.POST.get("team-string")

        g = geocoder.osm(location_string)

        #new_data = Data(team_name=team_string, latitude=g.lat, longitude=g.lng)
        #new_data.save()

    data = Data.objects.all()

    gps_data = pd.DataFrame(list(data.values('team_name','latitude','longitude')))
    map_center = [gps_data['latitude'].mean(), gps_data['longitude'].mean()]
    map_zoom = 12
    clustered_map = folium.Map(location=map_center, zoom_start=map_zoom)

    teams = set(gps_data['team_name'].unique())
    team_index = 0
    for team in teams:
        data_subset = gps_data[gps_data['team_name'] == team]
        #print(data_subset)
        clustered_map = plot_one_team_cluster(data_subset, colors[team_index], team, clustered_map)
        team_index += 1

    folium.Marker(location=[g.lat, g.lng]).add_to(clustered_map)

    heat_map = clustered_map._repr_html_()
    context = {
        'heat_map': heat_map
    }

    return render(request, 'dashboard/map_clustered.html', context)

    #return HttpResponseRedirect(reverse('map-clustered'))


def cluster(request):

    data = Data.objects.all()
    map_zoom = 12
    #No data inputed yet
    if len(data) == 0:
        clustered_map = folium.Map(location=[40.4406, -79.9959], zoom_start=map_zoom)
        heat_map = clustered_map._repr_html_()
        context = {
            'heat_map': heat_map
        }
        return render(request, 'dashboard/map_clustered.html', context)
    
    gps_data = pd.DataFrame(list(data.values('team_name','latitude','longitude')))
    map_center = [gps_data['latitude'].mean(), gps_data['longitude'].mean()]
    map_zoom = 12
    clustered_map = folium.Map(location=map_center, zoom_start=map_zoom)

    teams = set(gps_data['team_name'].unique())
    team_index = 0
    for team in teams:
        data_subset = gps_data[gps_data['team_name'] == team]
        #print(data_subset)
        clustered_map = plot_one_team_cluster(data_subset, colors[team_index], team, clustered_map)
        team_index += 1

    heat_map = clustered_map._repr_html_()
    context = {
        'heat_map': heat_map
    }

    return render(request, 'dashboard/map_clustered.html', context)

def uncluster(request):

    data = Data.objects.all()
    map_zoom = 12
    #No data inputed yet
    if len(data) == 0:
        unclustered_map = folium.Map(location=[40.4406, -79.9959], zoom_start=map_zoom)
        heat_map = unclustered_map._repr_html_()
        context = {
            'heat_map': heat_map
        }
        return render(request, 'dashboard/map_unclustered.html', context)
    
    gps_data = pd.DataFrame(list(data.values('team_name','latitude','longitude')))
    map_center = [gps_data['latitude'].mean(), gps_data['longitude'].mean()]
    unclustered_map = folium.Map(location=map_center, zoom_start=map_zoom)

    teams = set(gps_data['team_name'].unique())
    team_index = 0
    for team in teams:
        data_subset = gps_data[gps_data['team_name'] == team]
        unclustered_map = plot_one_team_uncluster(data_subset, colors[team_index], team, unclustered_map)
        team_index += 1

    heat_map = unclustered_map._repr_html_()
    context = {
        'heat_map': heat_map
    }

    return render(request, 'dashboard/map_unclustered.html', context)


def plot_one_team_uncluster(gps_data_subset, color, team_label, unclustered_map):

    # add points to the unclustered map
    for i, row in gps_data_subset.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            fill=True,
                            color=color,
                            fill_color=color,
                            fill_opacity=0.5,#).add_to(unclustered_map)
                            tooltip=team_label).add_to(unclustered_map)

    return unclustered_map

def plot_one_team_cluster(gps_data_subset, color, team_label, clustered_map):
    
    # find the optimal number of clusters to use for k-means
    coordinates = gps_data_subset[['latitude', 'longitude']].values
    X = np.array(coordinates)

    wcss = []
    for i in range(1, len(coordinates)):
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
                    'weight': weights, 
                    'team-name': team_label})

    print("Weighted GPS Data")
    print (weighted_gps_data)

    # --------------------------------------


    # Create a map with the markers sized by the weight of each center point
    for i, row in weighted_gps_data.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            radius=row['weight'] * 2, # CHANGE THIS WEIGHT
                            fill=True,
                            color=color,
                            fill_color=color,
                            fill_opacity=0.5,
                            tooltip=(team_label + ", " + str(int(row['weight'])))).add_to(clustered_map)
        
    return clustered_map