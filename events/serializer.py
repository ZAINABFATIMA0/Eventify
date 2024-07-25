from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import Category, Event, Schedule

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    location = serializers.JSONField()

    class Meta:
        model = Schedule
        fields = ['start_time', 'end_time', 'location']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance.location, Point):
            representation['location'] = f"({instance.location.x}, {instance.location.y})"
        return representation

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")
        
        location = data.get('location')
        if location:
            try:
                latitude, longitude = map(float, location.split(','))
                if latitude < -90 or latitude > 90:
                    raise serializers.ValidationError(
                        "Latitude must be between -90 and 90."
                    )
                if longitude < -180 or longitude > 180:
                    raise serializers.ValidationError(
                        "Longitude must be between -180 and 180."
                    )
            except ValueError:
                raise serializers.ValidationError("Invalid location format.")
            
        return data
    
class EventSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creator']

    def validate(self, data):
        registration_start_time = data.get('registration_start_time')
        registration_end_time = data.get('registration_end_time')
        event_type = data.get('type')
        meeting_link = data.get('meeting_link')
        schedules = data.get('schedules', [])

        if registration_start_time >= registration_end_time:
            raise serializers.ValidationError(
                "Registration end time should be after registration start time."
            )
        
        if event_type in ['HYBRID', 'ONSITE']:
            location_required = any(
                isinstance(schedule.get('location'), str)
                for schedule in schedules
            )
            if not location_required:
                raise serializers.ValidationError(
                    "Location with coordinates is required for hybrid and onsite events."
                )
        
        if event_type in ['HYBRID', 'ONLINE'] and not meeting_link:
            raise serializers.ValidationError(
                "Meeting link is required for online and hybrid events."
            )
        
        return data

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(**category_data)
        validated_data['category'] = category

        creator = self.context.get('creator')
        if not creator:
            raise serializers.ValidationError("Creator is not provided in context")
        validated_data['creator'] = creator

        event = Event.objects.create(**validated_data)

        schedules_data = validated_data.pop('schedules')
        for schedule_data in schedules_data:
            location_data = schedule_data.pop('location', {})
            try:
                latitude, longitude = map(float, location_data.split(','))
                location = Point(latitude, longitude)
            except ValueError:
                    location = None
            Schedule.objects.create(**schedule_data, event=event, location=location)

        return event
