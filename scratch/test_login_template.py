import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_project.settings')
django.setup()
from django.template import loader
from django.test import RequestFactory

rf = RequestFactory()
request = rf.get('/')
request.session = {}
request.user = None

tmpl = loader.get_template('login.html')
print('Template loaded successfully')
rendered = tmpl.render({}, request)
print('Rendered length:', len(rendered))
