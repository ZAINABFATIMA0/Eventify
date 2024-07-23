from django.db import models
from django.contrib.gis.db import models as model

from .choices import EventType


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    parent = models.ForeignKey(
        "events.Category", 
        related_name="categories", 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE
    )


class Event(models.Model):
    type = models.CharField(
        max_length=10,
        choices=EventType.choices,
        default=EventType.ONSITE,
    )
    name = models.CharField(max_length=32)
    registration_start_time = models.DateTimeField()
    registration_end_time = models.DateTimeField()
    seat_limit = models.PositiveIntegerField()
    description = models.TextField()
    meeting_link = models.URLField()

    category = models.ForeignKey(
        "events.Category", 
        related_name="events", 
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        "users.User", 
        related_name="events", 
        on_delete=models.CASCADE
    )


class Schedule(model.Model):
    start_time = model.DateTimeField()
    end_time = model.DateTimeField()
    location = model.PointField()

    event = models.ForeignKey(
        "events.Event", 
        related_name='schedules', 
        on_delete=models.CASCADE
    )
