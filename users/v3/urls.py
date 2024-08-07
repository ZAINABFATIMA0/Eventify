from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import RegistrationAPIView, EventListingAPIView, EventDashboardAPIView


urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user_register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('all-events/', EventListingAPIView.as_view(), name='events'),
    path('<int:pk>/dashboard/', EventDashboardAPIView.as_view(), name='dashbaord')
]
