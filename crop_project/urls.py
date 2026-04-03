from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),   # Home + Weather
    path('chatbot/', include('chatbot.urls')),
    path('soil/', include('soil.urls')),
    path('analysis/', include('analysis.urls')),
    path('disease/', include('disease_detection.urls')),
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),
    path('manifest.json', TemplateView.as_view(template_name="manifest.json", content_type='application/json'), name='manifest.json'),
]