from django.urls import path
from . import views

urlpatterns = [
    path('', views.soil_predict, name='soil_predict'),
    path('live/', views.live_soil_scan, name='live_soil_scan'),
]