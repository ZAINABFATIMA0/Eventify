from django.urls import path

from .views import create_event, list_event, list_category

urlpatterns = [
    path('create/', create_event, name='create_event'),
    path('listing/', list_event, name='list_event'),
    path('list-categories/', list_category, name='list_category')
]
