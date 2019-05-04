from datetime import datetime
from uuid import uuid4

from django.conf import settings
from django.db import models


def get_timestamp_after_10m() -> int:
    return int(datetime.now().timestamp()) + 600


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


class TokenModel(models.Model):
    token = models.CharField(max_length=256, primary_key=True)
    app = models.ForeignKey(AppModel, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.app.name} {self.student.number}'


class RefreshTokenModel(models.Model):
    refresh_token = models.CharField(max_length=256, primary_key=True)
    app = models.ForeignKey(AppModel, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.app.name} {self.student.number}'


class AccessTokenModel(models.Model):
    access_token = models.CharField(max_length=256, primary_key=True, unique=True)
    app = models.ForeignKey(AppModel, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expire_timestamp = models.IntegerField(default=get_timestamp_after_10m)

    def __str__(self):
        return f'{self.app.name} {self.student.number}'


class ServiceModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'


class AppServiceRelModel(models.Model):
    app = models.ForeignKey(AppModel, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.app}, {self.service}'

    class Meta:
        unique_together = (('app', 'service'),)
