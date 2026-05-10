import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_project.settings')
django.setup()

from django.contrib.auth.models import User

# This will create an admin account automatically
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Admin created!")
else:
    print("✅ Admin already exists!")
