from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import register, get_events, get_verified_registrations

urlpatterns = [
   path('register/', register, name='register'),
   path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
   path('all-events/', get_events, name='user_events'),
   path('<int:pk>/dashboard/', get_verified_registrations, name='get_verified_registrations'),
]
