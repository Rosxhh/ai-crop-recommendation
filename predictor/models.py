from django.db import models

class YieldPrediction(models.Model):
    rainfall = models.FloatField()
    temperature = models.FloatField()
    area = models.FloatField()
    predicted_yield = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Yield: {self.predicted_yield}"