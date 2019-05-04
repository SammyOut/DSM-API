from uuid import uuid4
from django.conf import settings
from django.db import models


def get_random_hash() -> str:
    return uuid4().hex


class AppModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=256, unique=True, default=get_random_hash)
    secret_key = models.CharField(max_length=256, unique=True, default=get_random_hash)
    app_url = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        return f'{self.name}'

