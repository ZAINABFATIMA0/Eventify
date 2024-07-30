from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User, Registration


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
        fields = ['email', 'event', 'is_verified', 'otp', 'otp_expiry']

    def create(self, validated_data):
        email = validated_data.get('email')
        event = validated_data.get('event')
        otp = validated_data.get('otp')
        otp_expiry = validated_data.get('otp_expiry')

        registration, created = Registration.objects.update_or_create(
            email=email,
            event=event,
            defaults={'otp': otp, 'otp_expiry': otp_expiry}
        )
        
        return registration