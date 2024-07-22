from django.db import models


class EmailLog(models.Model):
    email_type = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)

    recipient = models.ForeignKey(
        "users.Registrations", 
        related_name="email_log", 
        on_delete=models.CASCADE
    )
