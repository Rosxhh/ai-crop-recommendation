from django.urls import path
from . import views

from django.views.generic import RedirectView

urlpatterns = [
    path('', views.smart_analysis, name='smart_analysis'),
    path('disease/', views.disease_scan, name='disease_scan'),
    path('api/disease-markers/', views.disease_markers_api, name='disease_markers_api'),
    
    # Legacy URL Restoration (Redirects to Unified Analysis)
    path('yield/', RedirectView.as_view(pattern_name='smart_analysis', permanent=False)),
    path('recommend/', RedirectView.as_view(pattern_name='smart_analysis', permanent=False)),
]
