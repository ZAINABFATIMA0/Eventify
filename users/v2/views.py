from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event, Schedule
from events.serializer import EventSerializer
from users.models import Registration
from users.serializer import UserSerializer, VerifiedRegistrationsSerializer


class RegistrationView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.validated_data,
        )
    
class EventListingsView(APIView):

    def get(self, request):
        events = Event.objects.filter(creator=request.user)

        paginator = PageNumberPagination()
        events_page = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(events_page, many=True)
        response = paginator.get_paginated_response(serializer.data)
        
        return response
    
class VerifiedRegistrationsView(APIView):

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, creator=request.user)
    
        schedules = Schedule.objects.filter(event=event, is_active=True)
        schedule_data = []

        for schedule in schedules:
            verified_registrations = Registration.objects.filter(
                schedule=schedule, 
                is_verified=True
            )
            serializer = VerifiedRegistrationsSerializer(
                verified_registrations, 
                many=True
            )
            
            schedule_data.append({
                'schedule': schedule.id,
                'seats_left': schedule.seats_left,
                'registrations_count': verified_registrations.count(),
                'registered_users': serializer.data,
            })
        
        return Response(schedule_data)
