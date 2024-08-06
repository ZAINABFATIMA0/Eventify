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
    unregister_from_event_schedule, 
    verify_unregistration_otp
)

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('<int:event_id>/update/', update_event, name='update_event'),
    path('listing/', list_event, name='list_event'),
    path('<int:event_id>/', get_event, name='get_event'),
    path('<int:event_id>/schedules/', list_schedules, name='list_schedules'),
    path('schedule/<int:schedule_id>/register/', register_for_event_schedule, name='register_for_event_schedule'),
    path('schedule/<int:schedule_id>/verify-registration-otp/', verify_registration_otp, name='verify_registration_otp'),
    path('schedule/<int:schedule_id>/unregister/', unregister_from_event_schedule, name='unregister_for_event'),
    path('schedule/<int:schedule_id>/verify-unregistration-otp/', verify_unregistration_otp, name='verify_unregistration_otp'),
    path('list-categories/', list_category, name='list_category'),
]
