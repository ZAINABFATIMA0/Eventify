from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from events.filters import Filters
from events.models import Category, Event, Schedule
from events.serializer import CategorySerializer, EventSerializer, ScheduleSerializer, VerifyOTPSerializer
from users.models import Registration
from users.serializer import RegistrationSerializer, UnregistrationSerializer


class CreateEventView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UpdateEventView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_object(self):
        return get_object_or_404(Event, id=self.kwargs['pk'], creator=self.request.user)


class ListEventView(generics.ListAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    filterset_class = Filters


class ListSchedulesView(generics.ListAPIView):

    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        return Schedule.objects.filter(event=event, is_active=True)
      

class ListCategoryView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GetEventView(generics.RetrieveAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class RegisterForEventScheduleView(generics.CreateAPIView):

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        request.data['schedule'] = self.kwargs['pk']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Registration created successfully. Check your email for OTP"}, 
            status=status.HTTP_201_CREATED
        )


class VerifyRegistrationOTPView(generics.UpdateAPIView):

    queryset = Registration.objects.all()
    serializer_class = VerifyOTPSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            Registration,
            schedule_id=self.kwargs['pk'],
            email=self.request.data.get('email')
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        request.data['schedule'] = self.kwargs['pk']
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        instance.is_verified = True
        instance.otp = None
        instance.otp_expiry = None
        instance.save(update_fields=["is_verified", "otp", "otp_expiry"])

        return Response(
            {"detail": "OTP verified successfully"}, 
            status=status.HTTP_200_OK
        )


class UnregisterFromEventScheduleView(generics.CreateAPIView):

    queryset = Registration.objects.all()
    serializer_class = UnregistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        request.data['schedule'] = self.kwargs['pk']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "OTP sent to email for unregistering."}, 
            status=status.HTTP_200_OK
        )


class VerifyUnregistrationOTPView(generics.UpdateAPIView):

    queryset = Registration.objects.all()
    serializer_class = VerifyOTPSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            Registration,
            schedule_id=self.kwargs['pk'],
            email=self.request.data.get('email')
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        request.data['schedule'] = self.kwargs['pk']
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        instance.is_verified = False
        instance.otp = None
        instance.otp_expiry = None
        instance.save(update_fields=["is_verified", "otp", "otp_expiry"])

        return Response(
            {"detail": "OTP verified successfully"}, 
            status=status.HTTP_200_OK
        )
