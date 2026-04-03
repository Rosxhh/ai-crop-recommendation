from django.db import models

class DiseaseMarker(models.Model):
    disease_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    report_date = models.DateTimeField(auto_now_add=True)

    def __cl__(self):
        return f"{self.disease_name} at ({self.latitude}, {self.longitude})"
