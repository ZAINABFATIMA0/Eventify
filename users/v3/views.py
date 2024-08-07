from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from events.models import Event
from events.serializer import EventSerializer
from users.serializer import UserSerializer, VerifiedRegistrationsSerializer


class RegistrationAPIView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class EventListingAPIView(generics.ListAPIView):

    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)


class EventDashboardAPIView(generics.RetrieveAPIView):

    def get_queryset(self):
        return Event.objects.filter(id=self.kwargs['pk'], creator=self.request.user).prefetch_related(
            'schedules__registrations'
        )

    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()
        schedules = event.schedules.filter(is_active=True)
        schedule_data = []

        for schedule in schedules:
            verified_registrations = schedule.registrations.filter(is_verified=True)
            serializer = VerifiedRegistrationsSerializer(verified_registrations, many=True)
            
            schedule_data.append({
                'schedule': schedule.id,
                'seats_left': schedule.seats_left,
                'registrations_count': verified_registrations.count(),
                'registered_users': serializer.data,
            })
        
        return Response(schedule_data)
