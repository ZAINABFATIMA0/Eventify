from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from events.filters import Filters
from events.models import Category, Event, Schedule
from events.serializer import CategorySerializer, EventSerializer, ScheduleSerializer, VerifyOTPSerializer
from users.models import Registration
from users.serializer import RegistrationSerializer, UnregistrationSerializer

@api_view(['POST'])
def create_event(request):
    serializer = EventSerializer(
        data=request.data, 
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def update_event(request, event_id):

    event = get_object_or_404(Event, id=event_id, creator=request.user)
    serializer = EventSerializer(
        event,
        data=request.data, 
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
@permission_classes([AllowAny])
def list_schedules(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    schedules = Schedule.objects.filter(event=event, is_active=True)
    serializer = ScheduleSerializer(schedules, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def list_category(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_for_event_schedule(request, schedule_id):

    schedule = get_object_or_404(Schedule, id=schedule_id)
    request.data['schedule'] = schedule_id
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(
        {"message": "Registration created successfully. Check your email for OTP"}
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_registration_otp(request, schedule_id):
    
    request.data['schedule'] = schedule_id
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    registration = get_object_or_404(
        Registration, 
        email=serializer.validated_data['email'], 
        schedule_id=schedule_id
    )
    registration.is_verified = True
    registration.otp = None
    registration.otp_expiry = None
    registration.save(update_fields=["is_verified", "otp", "otp_expiry"])

    return Response({"message": "OTP/Email verified successfully"})


@api_view(['POST'])
@permission_classes([AllowAny])
def unregister_from_event_schedule(request, schedule_id):

    request.data['schedule'] = schedule_id
    serializer = UnregistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"message": "OTP sent to email for unregistering."})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_unregistration_otp(request, schedule_id):

    request.data['schedule'] = schedule_id
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    registration = get_object_or_404(
        Registration, 
        email=serializer.validated_data['email'], 
        schedule_id=schedule_id
    )
    
    registration.is_verified = False
    registration.otp = None
    registration.otp_expiry = None
    registration.save(update_fields=['is_verified', 'otp', 'otp_expiry'])
    
    return Response({"message": "Unregistered successfully."})
