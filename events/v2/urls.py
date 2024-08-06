from django.urls import path

from .views import (
    EventCreationAPIView, 
    EventUpdationAPIView, 
    EventDetailAPIView, 
    EventListingAPIView, 
    ScheduleListingAPIView, 
    CategoryListingAPIView, 
    EventScheduleRegistrationAPIView, 
    EventScheduleUnregistrationAPIView, 
    RegistrationOtpVerificationAPIView, 
    UnregistrationOtpVerificationAPIView,
)

urlpatterns = [
    path('create/', EventCreationAPIView.as_view(), name='create_event'),
    path('<int:event_id>/update/', EventUpdationAPIView.as_view(), name='update_event'),
    path('listing/', EventListingAPIView.as_view(), name='list_event'),
    path('<int:event_id>/', EventDetailAPIView.as_view(), name='get_event_details'),
    path('<int:event_id>/schedules/', ScheduleListingAPIView.as_view(), name='list_schedules'),
    path('schedule/<int:schedule_id>/register/', EventScheduleRegistrationAPIView.as_view(), name='register_for_event_schedule'),
    path('schedule/<int:schedule_id>/verify-registration-otp/', RegistrationOtpVerificationAPIView.as_view(), name='verify_registration_otp'),
    path('schedule/<int:schedule_id>/unregister/', EventScheduleUnregistrationAPIView.as_view(), name='unregister_from_event_schedule'),
    path('schedule/<int:schedule_id>/verify-unregistration-otp/', UnregistrationOtpVerificationAPIView.as_view(), name='verify_unregistration_otp'),
    path('list-categories/', CategoryListingAPIView.as_view(), name='list_category'),
]
