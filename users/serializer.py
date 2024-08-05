from datetime import timedelta
import random

from constance import config
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from .models import User, Registration
from events.tasks import send_registration_otp_email, send_unregistration_otp_email


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

        if not data.get('schedule').is_active:
            raise serializers.ValidationError(
                "Registration is not allowed for this schedule as it is inactive."
            )

        if data.get('schedule').seats_left <= 0:
           raise serializers.ValidationError("Registration is full for this event.")

        if not (data.get('schedule').registration_start_time 
                <= timezone.now() 
                <= data.get('schedule').registration_end_time):
            raise serializers.ValidationError("Registration has not opened or is closed.")
        return data
    
    def create(self, validated_data):
        registration, created = Registration.objects.update_or_create(
            email=validated_data.get('email'),
            schedule=validated_data.get('schedule'),
            defaults={
                'otp': random.randint(100000, 999999),
                'otp_expiry': timezone.now() + timedelta(minutes=config.OTP_EXPIRY_TIME)
            }
        )
        send_registration_otp_email.delay(registration.email, registration.otp, config.OTP_EXPIRY_TIME)
        return registration


class VerifiedRegistrationsSerializer(serializers.ModelSerializer):
   class Meta:
       model = Registration
       fields = ['email']


class UnregistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    schedule = serializers.IntegerField()

    def validate(self, data):
        registration = get_object_or_404(
            Registration,
            email=data['email'],
            schedule_id=data['schedule']
        )
        grace_period_end = (
            registration.schedule.registration_end_time 
            - timedelta(days=config.UNREGISTRATION_GRACE_PERIOD)
        )

        if timezone.now() > grace_period_end:
            raise serializers.ValidationError("Unregistration period has expired.")

        return data

    def create(self, validated_data):
        registration = get_object_or_404(
            Registration,
            email=validated_data['email'],
            schedule_id=validated_data['schedule']
        )

        registration.otp = random.randint(100000, 999999)
        registration.otp_expiry = timezone.now() + timedelta(minutes=config.OTP_EXPIRY_TIME)
        registration.save(update_fields=['otp', 'otp_expiry'])

        send_unregistration_otp_email.delay(registration.email, registration.otp, config.OTP_EXPIRY_TIME)

        return registration
