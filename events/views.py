from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import Filters
from .helpers import generate_otp_and_expiry
from .models import Category, Event
from .serializer import CategorySerializer, EventSerializer
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
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'})

    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_for_event(request, event_id):
    email = request.data.get('email')
    otp, otp_expiry = generate_otp_and_expiry()
    registration = {
        'email': email,
        'event': event_id,
        'otp': otp,
        'otp_expiry': otp_expiry
    }
    serializer = RegistrationSerializer(data=registration)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    send_otp_email.delay(email, otp)

    return Response({"message": "Registration created successfully"})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
        return Response({"error": "Both email and OTP must be provided"})
    try:
        registration = Registration.objects.get(email=email)
    except Registration.DoesNotExist:
        return Response({"error": "Registration not found"})
    
    if registration.otp_expiry < timezone.now():
        return Response({"error": "OTP has expired"})
    
    if registration.otp != otp:
        return Response({"error": "Invalid OTP"})
    
    registration.is_verified = True
    registration.otp = None  
    registration.save()
    
    return Response({"message": "OTP verified successfully"})
