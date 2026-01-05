from django.contrib import admin
from django.urls import path, include
from apps.dashboard.admin_site import school_admin_site
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', school_admin_site.urls),
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
]
