from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = (
        "student",
        "date",
        "status",
        "remark",
        "created_at",
    )

    list_filter = ("status", "date")
    search_fields = (
        "student__first_name",
        "student__last_name",
        "student__admission_number",
    )
    ordering = ("-date",)

    autocomplete_fields = ("student",)
    list_editable = ("status",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Student Info", {
            "fields": ("student",)
        }),
        ("Attendance Details", {
            "fields": ("date", "status", "remark")
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )
