from django.contrib import admin
from django.urls import path, include
from apps.dashboard.admin_site import school_admin_site


urlpatterns = [
    path('', school_admin_site.urls),
]
