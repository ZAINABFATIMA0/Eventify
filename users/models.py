from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    phone = models.CharField(max_length=32, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Registration(models.Model):
    email = models.EmailField(max_length=255)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    event = models.ForeignKey(
        "events.Event", 
        related_name='registrations', 
        on_delete=models.CASCADE,
    )
