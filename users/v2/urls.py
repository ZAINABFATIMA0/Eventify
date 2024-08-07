from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import RegistrationAPIView, EventListingAPIView, EventDashboardAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('all-events/', EventListingAPIView.as_view(), name='event_listing'),
    path('<int:event_id>/dashboard/', EventDashboardAPIView.as_view(), name='verified_registrations'),
]
