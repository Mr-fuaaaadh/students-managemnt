from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Student


@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone",
        "course",
        "is_active",
        "admission_date",
    )

    list_filter = (
        "course",
        "is_active",
        "admission_date",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    ordering = ("-admission_date",)

    readonly_fields = ("created_at", "updated_at", "admission_date")

    fieldsets = (
        ("Student Info", {
            "fields": (
                ("first_name", "last_name"),
                ("phone", "email"),
                "date_of_birth",
            )
        }),
        ("Academic Info", {
            "fields": (
                "course",
                "admission_date",
            )
        }),
        ("Address", {
            "fields": ("address",)
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )

    @admin.display(description="Name", ordering="first_name")
    def full_name(self, obj):
        return obj.full_name
