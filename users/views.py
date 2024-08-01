from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializer import UserSerializer, VerifiedRegistrationsSerializer
from events.serializer import EventSerializer
from events.models import Event
from users.models import Registration

@api_view(['POST'])
@permission_classes([AllowAny]) 
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        serializer.validated_data,
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request):
   
   events = Event.objects.filter(creator=request.user)

   paginator = PageNumberPagination()
   events_page = paginator.paginate_queryset(events, request)
   serializer = EventSerializer(events_page, many=True)
   response = paginator.get_paginated_response(serializer.data)
  
   return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_verified_registrations(request, pk):
   
   event = get_object_or_404(Event, id=pk, creator=request.user)
  
   verified_registrations = Registration.objects.filter(event=event, is_verified=True)
   serializer = VerifiedRegistrationsSerializer(verified_registrations, many=True)
  
   return Response({
        'seats_left': event.seat_limit - verified_registrations.count(),
        'registrations_count': verified_registrations.count(),
        'registered_users': serializer.data,
    })
