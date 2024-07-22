from django.db import models
from django.contrib.gis.db import models as model


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    
    parent = models.ForeignKey(
        "events.Category", 
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
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default=ONSITE,
    )

    registration_start_time = models.DateTimeField()
    registration_end_time = models.DateTimeField()

    description = models.TextField()

    meeting_link = models.URLField()
    unique_link = models.URLField(unique=True)

    seat_limit = models.PositiveIntegerField()

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
