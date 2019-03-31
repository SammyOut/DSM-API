from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


def get_timestamp_after_10m() -> int:
    return int(datetime.now().timestamp()) + 600


class StudentModel(AbstractUser):
    uuid = models.CharField(unique=True)
    number = models.IntegerField(unique=True)
    name = models.CharField()

    def __str__(self):
        return f'{self.number} {self.name}'

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class AppModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True)
    description = models.CharField()
    owner = models.OneToOneField(StudentModel, on_delete=True)
    client_id = models.CharField(unique=True)
    secret_key = models.CharField(unique=True)

    def __str__(self):
        return f'{self.name}'


class RefreshTokenModel(models.Model):
    refresh_token = models.CharField(primary_key=True)
    app = models.OneToOneField(AppModel, on_delete=models.CASCADE)
    student = models.OneToOneField(StudentModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.app.name} {self.student.number}'


class AccessTokenModel(models.Model):
    access_token = models.CharField(primary_key=True, unique=True)
    app = models.OneToOneField(AppModel, on_delete=models.CASCADE)
    student = models.OneToOneField(StudentModel, on_delete=models.CASCADE)
    expire_timestamp = models.IntegerField(default=get_timestamp_after_10m)

    def __str__(self):
        return f'{self.app.name} {self.student.number}'


class ServiceModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True)
    description = models.CharField()

    def __str__(self):
        return f'{self.name}'


class AppServiceRelModel(models.Model):
    app = models.OneToOneField(AppModel, primary_key=True, on_delete=True)
    service = models.OneToOneField(ServiceModel, primary_key=True, on_delete=True)

    def __str__(self):
        return f'{self.app}, {self.service}'

    class Meta:
        unique_together = (('app', 'service'),)
