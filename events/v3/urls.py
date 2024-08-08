from django.urls import path

from .views import (
    CreateEventView,
    UpdateEventView,
    ListEventView,
    ListSchedulesView,
    ListCategoryView,
    GetEventView,
    RegisterForEventScheduleView,
    VerifyRegistrationOTPView,
    UnregisterFromEventScheduleView,
    VerifyUnregistrationOTPView
)

urlpatterns = [
    path('', CreateEventView.as_view(), name='create_event'),
    path('<int:pk>/', UpdateEventView.as_view(), name='update_event'),
    path('<int:pk>/detail/', GetEventView.as_view(), name='event_detail'),
    path('listing/', ListEventView.as_view(), name='list_events'),
    path('<int:pk>/schedules/', ListSchedulesView.as_view(), name='list_schedules'),
    path('categories/', ListCategoryView.as_view(), name='list_category'),
    path('schedule/<int:pk>/register/', RegisterForEventScheduleView.as_view(), name='register_for_event_schedule'),
    path('schedule/<int:pk>/verify-registration-otp/', VerifyRegistrationOTPView.as_view(), name='verify_registration_otp'),
    path('schedule/<int:pk>/unregister/', UnregisterFromEventScheduleView.as_view(), name='unregister_from_event_schedule'),
    path('schedule/<int:pk>/verify-unregistration-otp/', VerifyUnregistrationOTPView.as_view(), name='verify_unregistration_otp'),
]
