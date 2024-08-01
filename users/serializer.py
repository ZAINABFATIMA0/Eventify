from datetime import timedelta
import random

from constance import config
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from .models import User, Registration
from events.tasks import send_otp_email, send_unregistration_email


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'password', 'confirm_password', 'phone', 'first_name', 'last_name'
        )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'

    def validate(self, data):
        if not (data.get('event').registration_start_time 
                <= timezone.now() 
                <= data.get('event').registration_end_time):
            raise serializers.ValidationError("Registration has not opened or is closed.")
        return data
    
    def create(self, validated_data):
        registration, created = Registration.objects.update_or_create(
            email=validated_data.get('email'),
            event=validated_data.get('event'),
            defaults={
                'otp': random.randint(100000, 999999),
                'otp_expiry': timezone.now() + timedelta(minutes=config.OTP_EXPIRY_TIME)
            }
        )
        send_otp_email.delay(registration.email, registration.otp, config.OTP_EXPIRY_TIME)
        return registration


class VerifiedRegistrationsSerializer(serializers.ModelSerializer):
   class Meta:
       model = Registration
       fields = ['email']


class UnregisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    event = serializers.IntegerField()

    def validate(self, data):
        registration = get_object_or_404(
            Registration,
            email=data['email'],
            event_id=data['event']
        )
        grace_period_end = (
            registration.event.registration_end_time 
            - timedelta(days=config.UNREGISTRATION_GRACE_PERIOD)
        )

        if timezone.now() > grace_period_end:
            raise serializers.ValidationError("Unregistration period has expired.")

        return data

    def create(self, validated_data):
        registration = get_object_or_404(
            Registration,
            email=validated_data['email'],
            event_id=validated_data['event']
        )

        registration.otp = random.randint(100000, 999999)
        registration.otp_expiry = timezone.now() + timedelta(minutes=config.OTP_EXPIRY_TIME)
        registration.save(update_fields=['otp', 'otp_expiry'])

        send_unregistration_email.delay(registration.email, registration.otp, config.OTP_EXPIRY_TIME)

        return registration
