from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from .models import Category, Event, Schedule
from .tasks import send_update_event_email
from users.models import Registration


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    location = serializers.JSONField()
    seats_left = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'type', 'start_time', 'end_time', 'registration_start_time', 
                  'registration_end_time', 'location', 'seat_limit', 'meeting_link', 'seats_left'
        ]

    def get_seats_left(self, obj):
       return obj.seats_left

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance.location, Point):
            representation['location'] = f"({instance.location.x}, {instance.location.y})"
        return representation

    def validate(self, data):

        if data['type'] in ['HYBRID', 'ONSITE']:
            location =  (
                isinstance(data.get('location'), dict) and 'coordinates' in data.get('location')
            )
            if not location:
                raise serializers.ValidationError(
                    "Location with coordinates is required for hybrid and onsite events."
                )

        if data['type'] in ['HYBRID', 'ONLINE'] and not data['meeting_link']:
            raise serializers.ValidationError(
                "Meeting link is required for online and hybrid events."
            )
        
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        
        if data['registration_start_time'] >= data['registration_end_time']:
            raise serializers.ValidationError(
                "Registration end time should be after registration start time."
            )

        if data['location']:
            try:
                coordinates = data['location'].get('coordinates')
                if len(coordinates) == 2:
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

    def update(self, instance, validated_data):

        new_schedules = validated_data.pop('schedules', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_schedules = instance.schedules.filter(is_active=True)

        for index in range(len(new_schedules)):
            location_data = new_schedules[index].pop('location', {})
            latitude, longitude = location_data.get('coordinates', [0, 0])
            location = Point(latitude, longitude)

            if index < len(existing_schedules):
                existing_schedule = existing_schedules[index]
                for attr, value in new_schedules[index].items():
                    setattr(existing_schedule, attr, value)
                existing_schedule.location = location
                existing_schedule.save()
            else:
                Schedule.objects.create(event=instance, location=location, **new_schedules[index])
        
        schedules_to_delete = existing_schedules[len(new_schedules):]
        for schedule in schedules_to_delete:
            schedule.is_active = False
            schedule.save()

        active_schedules = Schedule.objects.filter(event=instance, is_active=True)
        verified_registrations = Registration.objects.filter(schedule__in=active_schedules, is_verified=True)
        for registration in verified_registrations:
            send_update_event_email.delay(registration.email, instance.name, instance.id)   

        return instance

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            creator = request.user
        
        validated_data['creator'] = creator
        schedules = validated_data.pop('schedules')

        event = Event.objects.create(**validated_data)

        for schedule in schedules:
            location = schedule.pop('location', {})
            try:
                coordinates = location.get('coordinates', [0, 0])
                latitude, longitude = coordinates
                location = Point(latitude, longitude)
            except (ValueError, TypeError):
                location = None
            Schedule.objects.create(**schedule, event=event, location=location)

        return event
 
  
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    schedule = serializers.IntegerField() 

    def validate(self, data):

        registration = get_object_or_404(
        Registration, 
        email=data.get('email'), 
        schedule_id=data.get('schedule')
        )
          
        if registration.otp != data.get('otp'):
            raise serializers.ValidationError({"otp": "Invalid OTP"})

        if registration.otp_expiry < timezone.now():
            raise serializers.ValidationError({"otp": "OTP has expired"})
      
        return data
