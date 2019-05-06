from django.db import models


class ServiceModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'
