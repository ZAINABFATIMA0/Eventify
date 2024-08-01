from django.urls import path

from .views import (
    create_event, 
    list_event, 
    get_event, 
    register_for_event, 
    verify_registration_otp,
    list_category,
    unregister_from_event, 
    verify_unregistration_otp
)

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('listing/', list_event, name='list_event'),
    path('<int:pk>/', get_event, name='get_event'),
    path('<int:pk>/register/', register_for_event, name='register_for_event'),
    path('<int:pk>/verify-registration-otp/', verify_registration_otp, name='verify_registration_otp'),
    path('<int:pk>/unregister/', unregister_from_event, name='unregister_for_event'),
    path('<int:pk>/verify-unregistration-otp/', verify_unregistration_otp, name='verify_unregistration_otp'),
    path('list-categories/', list_category, name='list_category'),
]
