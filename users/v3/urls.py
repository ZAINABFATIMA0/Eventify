from django.urls import path

from .views import RegistrationAPIView, EventListingAPIView, EventDashboardAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user_register'),
    path('all-events/', EventListingAPIView.as_view(), name='events'),
    path('<int:pk>/dashboard/', EventDashboardAPIView.as_view(), name='dashbaord')
]
