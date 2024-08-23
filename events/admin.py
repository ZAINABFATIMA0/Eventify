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
        'name',
        'description',
        'category',
        'creator',
    )
    search_fields = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'type',
        'start_time', 
        'end_time', 
        'registration_start_time',
        'registration_end_time',
        'seat_limit',
        'location',
        'meeting_link',
        'event', 
        'is_active'
    )
    list_filter = (
        'start_time', 
        'end_time',
        'registration_start_time',
        'registration_end_time',
        'seat_limit',
    )
