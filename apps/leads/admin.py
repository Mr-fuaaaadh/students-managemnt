from django.contrib import admin, messages
from unfold.admin import ModelAdmin

from .models import Lead, LeadStatus
from .services import convert_lead_to_student


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "phone",
        "course",
        "status",
        "assigned_to",
        "created_at",
    )
    list_display_links = ("name",)
    list_filter = ("status", "course", "assigned_to", "created_at")
    search_fields = ("name", "phone", "email")
    ordering = ("-created_at",)

    readonly_fields = ("created_at", "updated_at", "converted_at")

    fieldsets = (
        ("Lead Info", {"fields": ("name", "phone", "email")}),
        ("Course Interest", {"fields": ("course",)}),
        ("Sales Handling", {"fields": ("assigned_to", "status", "source")}),
        ("Remarks", {"fields": ("remarks",)}),
        ("Conversion", {"fields": ("converted_at",)}),
        ("System Info", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    actions = ["convert_to_student"]

    @admin.action(description="Convert selected leads to Students")
    def convert_to_student(self, request, queryset):
        success = 0
        errors = 0

        for lead in queryset.exclude(status=LeadStatus.CONVERTED):
            try:
                convert_lead_to_student(lead)
                success += 1
            except Exception as e:
                errors += 1
                self.message_user(request, f"{lead.name}: {str(e)}", messages.ERROR)

        if success:
            self.message_user(
                request,
                f"{success} lead(s) converted to students successfully.",
                messages.SUCCESS,
            )

        if errors:
            self.message_user(
                request,
                f"{errors} lead(s) could not be converted.",
                messages.WARNING,
            )
