from django.db import models

class Devices(models.Model):
    name = models.CharField(max_length=20)
    activated = models.BooleanField(default=True)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

