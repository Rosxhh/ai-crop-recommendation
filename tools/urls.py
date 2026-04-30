from django.urls import path
from . import views

urlpatterns = [
    path('fertilizer/', views.fertilizer_calc, name='fertilizer_calc'),
    path('profit/',     views.profit_calc,     name='profit_calc'),
    path('calendar/',   views.crop_calendar,   name='crop_calendar'),
    path('market/',     views.market_prices,   name='market_prices'),
    path('schemes/',    views.schemes,         name='schemes'),
]
