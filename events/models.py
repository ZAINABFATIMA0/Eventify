from django.db import models
from django.contrib.gis.db import models as model

from .choices import EventType
from users.models import Registration


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
    name = models.CharField(max_length=32)
    description = models.TextField()

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
    is_active = model.BooleanField(default=True)
    type = models.CharField(
        max_length=10,
        choices=EventType.choices,
        default=EventType.ONSITE,
    )
    start_time = model.DateTimeField()
    end_time = model.DateTimeField()
    registration_start_time = model.DateTimeField()
    registration_end_time = model.DateTimeField()
    location = model.PointField(blank=True, null=True)
    seat_limit = model.PositiveIntegerField(blank=True, null=True)
    meeting_link = model.URLField(blank=True, null=True)

    event = models.ForeignKey(
        "events.Event", 
        related_name='schedules', 
        on_delete=models.CASCADE
    )

    @property
    def seats_left(self):
        if self.seat_limit is not None:
            total_registrations = Registration.objects.filter(schedule=self, is_verified=True).count()
            return self.seat_limit - total_registrations
        return None  
