from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Course


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "duration_months",
        "fees",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "duration_months",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
    )

    ordering = ("name",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Course Info", {
            "fields": ("name", "code", "description")
        }),
        ("Academic Details", {
            "fields": ("duration_months", "fees")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )
