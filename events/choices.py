from django.db import models


class EventType(models.TextChoices):
        ONSITE = 'ONSITE', 'Onsite'
        ONLINE = 'ONLINE', 'Online'
        HYBRID = 'HYBRID', 'Hybrid'