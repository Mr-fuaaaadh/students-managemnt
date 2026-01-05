from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Staff
from .forms import StaffAdminForm  # optional custom form


@admin.register(Staff)
class StaffAdmin(UserAdmin):
    form = StaffAdminForm
    model = Staff

    list_display = (
        "id",
        "username",
        "full_name",
        "email",
        "role",
        "is_active",
        "date_joined",
    )

    list_filter = ("role", "is_active", "date_joined")
    ordering = ("-date_joined",)
    search_fields = ("username", "first_name", "last_name", "email")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "phone", "address")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    def full_name(self, obj):
        return obj.get_full_name() or obj.username
