from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.home, name='home'),
    path('satellite/', views.satellite_map, name='satellite_map'),
    path('weather/', views.weather_view, name='weather'),
    path('security/history/', views.login_history_view, name='login_history'),
    path('health/', views.health_check, name='health_check'),
]