from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.uncluster, name='map-unclustered'),
    path('cluster/', views.cluster, name='map-clustered'),
    path('add-location/', views.add_location, name='add-location'),
    path('thanks/', views.thanks, name='thanks'),
]