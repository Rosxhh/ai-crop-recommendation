from django.db import models

class ChatMessage(models.Model):
    session_id = models.CharField(max_length=100)
    role = models.CharField(max_length=10) # 'user' or 'assistant'
    text = models.TextField()
    image_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} ({self.session_id}): {self.text[:30]}"

