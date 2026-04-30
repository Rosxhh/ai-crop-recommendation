import os
import sys
import django
import json
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_project.settings')
django.setup()

from django.test import RequestFactory
from chatbot.views import chatbot_api
from chatbot.models import ChatMessage
from django.contrib.sessions.middleware import SessionMiddleware

# Create a mock session ID and history
sid = str(uuid.uuid4())
ChatMessage.objects.create(session_id=sid, role='user', text='Hello')
ChatMessage.objects.create(session_id=sid, role='user', text='hi')

factory = RequestFactory()
request = factory.post(f'/chatbot/api/?session_id={sid}', data=json.dumps({
    "message": "hi again",
    "image": None,
    "language": "English"
}), content_type='application/json')

middleware = SessionMiddleware(lambda req: None)
middleware.process_request(request)
request.session.save()

try:
    response = chatbot_api(request)
    print("STATUS:", response.status_code)
    print("CONTENT:", response.content)
except Exception as e:
    print("EXCEPTION:", repr(e))
