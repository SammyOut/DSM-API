from django.contrib.auth.models import AbstractUser
from django.db import models


class StudentModel(AbstractUser):
    uuid = models.CharField(max_length=256, unique=True, null=True)
    number = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'{self.number} {self.name}'
