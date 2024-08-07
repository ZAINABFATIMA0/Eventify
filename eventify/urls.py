from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.v1.urls")),
    path("api/v2/users/", include("users.v2.urls")),
    path("api/v1/events/", include("events.v1.urls")),
    path("api/v2/events/", include("events.v2.urls")),
    path("communications/", include("communications.urls")),
]
