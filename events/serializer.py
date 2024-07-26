from django.contrib.gis.geos import Point
from rest_framework import serializers

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
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        
        if data['location']:
            try:
                coordinates = data['location'].get('coordinates')
                if coordinates and len(coordinates) == 2:
                    latitude, longitude = coordinates
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

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['creator']

    def validate(self, data):
        if data['registration_start_time'] >= data['registration_end_time']:
            raise serializers.ValidationError(
                "Registration end time should be after registration start time."
            )

        if data['type'] in ['HYBRID', 'ONSITE']:
            location = any(
                isinstance(schedule.get('location'), dict) and 'coordinates' in schedule['location']
                for schedule in data['schedules']
            )
            if not location:
                raise serializers.ValidationError(
                    "Location with coordinates is required for hybrid and onsite events."
                )

        if data['type'] in ['HYBRID', 'ONLINE'] and not data['meeting_link']:
            raise serializers.ValidationError(
                "Meeting link is required for online and hybrid events."
            )
        
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            creator = request.user
        
        validated_data['creator'] = creator
        schedules = validated_data.pop('schedules')

        event = Event.objects.create(**validated_data)

        for schedule in schedules:
            location_data = schedule.pop('location', {})
            try:
                coordinates = location_data.get('coordinates', [0, 0])
                latitude, longitude = coordinates
                location = Point(longitude, latitude)
            except (ValueError, TypeError):
                location = None
            Schedule.objects.create(**schedule, event=event, location=location)


        return event
