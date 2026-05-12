import os
import sys
# Ensure the inner project directory is on the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_project.settings')
import django
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()
response = client.get(reverse('login'))
print('Status Code:', response.status_code)
print('Content snippet:', response.content[:200].decode('utf-8', errors='ignore'))
