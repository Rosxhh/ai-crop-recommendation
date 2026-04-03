from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('satellite/', views.satellite_map, name='satellite_map'),
    path('weather/', views.weather_view, name='weather'),

]