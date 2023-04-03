from django.shortcuts import render
from .models import Data

from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import folium
import random


# Create your views here.
def index(request):
    data = Data.objects.all()

    map_zoom = 12

    gps_data = pd.DataFrame(list(Data.objects.all().values('team_name','latitude','longitude')))

    map_center = [gps_data['latitude'].mean(), gps_data['longitude'].mean()]

    data_subset = gps_data[gps_data['team_name'] == 'A']

    color = 'red'

    heat_map = folium.Map(location=map_center, zoom_start=map_zoom)

    for i, row in data_subset.iterrows():
        folium.CircleMarker([row['latitude'], row['longitude']],
                            fill=True,
                            color=color,
                            fill_color=color,
                            fill_opacity=0.5,
                            tooltip='A').add_to(heat_map)


    heat_map = heat_map._repr_html_()
    context = {
        'heat_map': heat_map
    }

    return render(request, 'dashboard/index.html', context)