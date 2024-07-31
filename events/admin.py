from django.contrib import admin

from .models import Category, Event, Schedule


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'name',
        'registration_start_time',
        'registration_end_time',
        'seat_limit',
        'description',
        'meeting_link',
        'category',
        'creator',
    )
    list_filter = ('registration_start_time', 'registration_end_time')
    search_fields = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'location', 'event')
    list_filter = ('start_time', 'end_time')
