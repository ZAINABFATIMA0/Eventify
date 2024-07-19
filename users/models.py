from django.db import models
from django.contrib.auth.models import AbstractUser

from events.models import Event


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=32, unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"


class Registrations(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    event = models.ForeignKey(
        Event, 
        related_name='registrations', 
        on_delete=models.CASCADE
    )
