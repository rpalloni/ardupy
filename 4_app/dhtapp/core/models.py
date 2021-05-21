from django.db import models

class SensorData(models.Model):
    time = models.DateTimeField(auto_now=True)
    data = models.JSONField() # django >= 3.1
