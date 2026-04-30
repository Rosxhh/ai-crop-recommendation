from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_crop, name='recommend'),
    path('rapid/', views.rapid_recommend, name='rapid_recommend'),
    path('history/', views.history_view, name='recommendation_history'),
    path('history/<int:report_id>/', views.report_detail, name='report_detail'),
    path('history/delete/<int:item_id>/', views.delete_history, name='delete_history'),
]