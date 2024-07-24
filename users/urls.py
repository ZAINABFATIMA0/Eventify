from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]
