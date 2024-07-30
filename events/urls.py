from django.urls import path

from .views import create_event, list_event, get_event, register_for_event, verify_otp, list_category

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('listing/', list_event, name='list_event'),
    path('<int:event_id>/', get_event, name='get_event'),
    path('<int:event_id>/register/', register_for_event, name='register_for_event'),
    path('<int:event_id>/verify-otp/', verify_otp, name='verify_otp'),
    path('list-categories/', list_category, name='list_category'),
]
