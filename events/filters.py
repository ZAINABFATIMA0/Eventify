from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import django_filters

from .models import Event, Category


class EventFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    registration_start_date = django_filters.IsoDateTimeFilter(
        field_name='registration_start_time', lookup_expr='gte'
    )
    registration_end_date = django_filters.IsoDateTimeFilter(
        field_name='registration_end_time', lookup_expr='lte'
    )
    event_start_date = django_filters.IsoDateTimeFilter(
        field_name='schedules__start_time', lookup_expr='gte'
    )
    event_end_date = django_filters.IsoDateTimeFilter(
        field_name='schedules__end_time', lookup_expr='lte'
    )
    location = django_filters.CharFilter(method='filter_by_location')

    class Meta:
        model = Event
        fields = [
            'name', 'category', 'registration_start_date', 
            'registration_end_date', 'event_start_date', 'event_end_date', 'location'
        ]

    def filter_by_location(self, queryset, name, value):
        try:
            latitude, longitude = map(float, value.split(','))
            user_location = Point(latitude, longitude, srid=4326)
            distance = 5000
            return queryset.annotate(
                distance=Distance('schedules__location', user_location)
            ).filter(distance__lte=distance)
        except (ValueError, TypeError):
            return queryset
