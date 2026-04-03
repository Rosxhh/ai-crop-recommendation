from django.urls import path
from . import views

urlpatterns = [
    path('', views.scan_page, name='disease_scan'),
    path('predict/', views.predict_disease_api, name='predict_disease'),
]
