from django.db import models

from users.models import Registrations


class Email_log(models.Model) :
    email_type = models.CharField (max_length=255)
    time_stamp = models.DateTimeField()
    subject = models.CharField (max_length=255)
    body = models.CharField (max_length=255)
    recipient = models.ForeignKey(
        Registrations, 
        related_name="email_log", 
        on_delete=models.CASCADE
    )
