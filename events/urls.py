from django.urls import path

from .views import (
    create_event,
    update_event, 
    list_event, 
    get_event,
    list_schedules,
    register_for_event_schedule, 
    verify_registration_otp,
    list_category,
    unregister_from_event, 
    verify_unregistration_otp
)

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('<int:pk>/update/', update_event, name='update_event'),
    path('listing/', list_event, name='list_event'),
    path('<int:pk>/', get_event, name='get_event'),
    path('<int:pk>/schedules/', list_schedules, name='list_schedules'),
    path('<int:event_id>/schedule/<int:schedule_id>/register/', register_for_event_schedule, name='register_for_event_schedule'),
    path('<int:pk>/verify-registration-otp/', verify_registration_otp, name='verify_registration_otp'),
    path('<int:pk>/unregister/', unregister_from_event, name='unregister_for_event'),
    path('<int:pk>/verify-unregistration-otp/', verify_unregistration_otp, name='verify_unregistration_otp'),
    path('list-categories/', list_category, name='list_category'),
]
