from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import StudentFee, FeePayment, FeeLedger, FeeStatus, LedgerType


# -----------------------------
# Inline FeePayment for StudentFee
# -----------------------------
class FeePaymentInline(TabularInline):
    model = FeePayment
    extra = 0
    fields = ("amount", "collected_by", "reference_no", "remarks", "is_active", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("collected_by",)


# -----------------------------
# StudentFee Admin
# -----------------------------
@admin.register(StudentFee)
class StudentFeeAdmin(ModelAdmin):
    list_display = (
        "student",
        "final_fee",
        "paid_amount",
        "due_amount",
        "colored_status",
        "view_payments",
        "view_ledger",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("student__full_name", "student__phone")
    ordering = ("-created_at",)
    autocomplete_fields = ("student",)
    inlines = [FeePaymentInline]

    readonly_fields = (
        "status",
        "paid_amount",
        "due_amount",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Student", {"fields": ("student",)}),
        ("Fee Details", {"fields": ("total_fee", "discount", "final_fee")}),
        ("Summary", {"fields": ("paid_amount", "due_amount", "status")}),
        ("System Info", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    # Lock student field after creation
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("student",)
        return self.readonly_fields

    # -----------------------------
    # Status colored box
    # -----------------------------
    def colored_status(self, obj):
        color_map = {
            FeeStatus.PENDING: "red",
            FeeStatus.PARTIAL: "orange",
            FeeStatus.PAID: "green",
        }
        color = color_map.get(obj.status, "black")
        return format_html(
            '<b style="color: {};">{}</b>', color, obj.get_status_display()
        )
    colored_status.short_description = "Status"
    colored_status.admin_order_field = "status"

    # -----------------------------
    # View buttons/links for payments and ledger
    # -----------------------------
    def view_payments(self, obj):
        url = reverse("admin:fees_feepayment_changelist") + f"?student_fee__id__exact={obj.id}"
        return format_html('<a class="button" href="{}"> Payments</a>', url)
    view_payments.short_description = "Fee Payments"

    def view_ledger(self, obj):
        url = reverse("admin:fees_feeledger_changelist") + f"?student__id__exact={obj.student.id}"
        return format_html('<a class="button" href="{}"> Ledger</a>', url)
    view_ledger.short_description = "Fee Ledger"


# -----------------------------
# FeePayment Admin
# -----------------------------
@admin.register(FeePayment)
class FeePaymentAdmin(ModelAdmin):
    list_display = (
        "student_fee",
        "amount",
        "payment_date",
        "collected_by",
        "is_active",
    )
    list_filter = ("payment_date", "collected_by", "is_active")
    search_fields = (
        "student_fee__student__full_name",
        "student_fee__student__phone",
        "reference_no",
    )
    autocomplete_fields = ("student_fee", "collected_by")


# -----------------------------
# FeeLedger Admin
# -----------------------------
@admin.register(FeeLedger)
class FeeLedgerAdmin(ModelAdmin):
    list_display = (
        "student",
        "entry_type",
        "debit",
        "credit",
        "balance",
        "created_at",
    )
    list_filter = ("entry_type", "created_at")
    search_fields = ("student__full_name", "student__phone")
    readonly_fields = (
        "student",
        "student_fee",
        "payment",
        "entry_type",
        "description",
        "debit",
        "credit",
        "balance",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
