from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Event
from .serializer import EventSerializer

@api_view(['POST'])
def create_event(request):
    serializer = EventSerializer(
        data=request.data, context={'creator': request.user}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        serializer.validated_data
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
