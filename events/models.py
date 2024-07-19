from django.db import models
from django.contrib.gis.db import models

from users.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "Category", 
        related_name="categories", 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
    )


class Event(models.Model):
    ONSITE = 'On-site'
    ONLINE = 'Online'
    HYBRID = 'Hybrid'
    
    EVENT_TYPE_CHOICES = [
        (ONSITE, 'On-site'),
        (ONLINE, 'Online'),
        (HYBRID, 'Hybrid'),
    ]

    name = models.CharField(max_length=32)
    description = models.TextField()
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default=ONSITE,
    )
    registration_start_time = models.DateTimeField()
    registration_end_time = models.DateTimeField()
    meeting_link = models.URLField()
    seat_limit = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, 
        related_name="events", 
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User, 
        related_name="events", 
        on_delete=models.CASCADE
    )


class Schedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.PointField()
    event = models.ForeignKey(
        Event, 
        related_name='schedules', 
        on_delete=models.CASCADE
    )
