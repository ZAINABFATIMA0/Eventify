from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import Filters
from .models import Category, Event
from .serializer import CategorySerializer, EventSerializer, VerifyOTPSerializer
from .tasks import send_otp_email
from users.models import Registration
from users.serializer import RegistrationSerializer

@api_view(['POST'])
def create_event(request):
    serializer = EventSerializer(
        data=request.data, 
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_event(request):
    events = Event.objects.all()

    filterset = Filters(request.GET, queryset=events)
    if filterset.is_valid():
        events = filterset.qs

    paginator = PageNumberPagination()
    events_page = paginator.paginate_queryset(events, request)
    serializer = EventSerializer(events_page, many=True)
    response = paginator.get_paginated_response(serializer.data)

    return response

@api_view(['GET'])
def list_category(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_for_event(request, event_id):
  
    serializer = RegistrationSerializer(
        data={
            'email': request.data['email'],
            'event': event_id
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"message": "Registration created successfully"})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request, event_id):

    serializer = VerifyOTPSerializer(
        data={
            'email': request.data.get('email'),
            'otp': request.data.get('otp'),
            'event': event_id,
        }
    )
    serializer.is_valid(raise_exception=True)

    registration = get_object_or_404(
        Registration, 
        email=serializer.validated_data['email'], 
        event_id=event_id
    )
    serializer.update(registration, serializer.validated_data)

    return Response({"message": "OTP verified successfully"})
