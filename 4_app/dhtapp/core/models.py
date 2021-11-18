from django.db import models

class SensorData(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    data = models.JSONField() # django >= 3.1
