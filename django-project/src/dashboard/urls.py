from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.uncluster, name='map-unclustered'),
    path('cluster/', views.cluster, name='map-clustered'),
    path('add-location/', views.add_location, name='add-location'),
    path('thanks/', views.thanks, name='thanks'),

    #these are used by the buttons
    path('addRandomCoords/', views.add_random_coords, name='addRandomCoords'),
    path('submitInfo/', views.submit_user_info, name='submitInfo'),
    path('routePath/', views.route, name='routePath'),
]