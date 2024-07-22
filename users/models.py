from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=32, unique=True, blank=True, null=True)

    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Registrations(models.Model):
    email = models.EmailField(max_length=255)

    event = models.ForeignKey(
        "events.Event", 
        related_name='registrations', 
        on_delete=models.CASCADE,
    )
