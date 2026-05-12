import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()
response = client.get(reverse('login'))
print('Status Code:', response.status_code)
print('Content snippet:', response.content[:200].decode('utf-8', errors='ignore'))
