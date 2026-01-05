from unfold.sites import UnfoldAdminSite as AdminSite
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.admin.models import LogEntry
from django.core.paginator import Paginator

from apps.students.models import Student
from apps.staff.models import Staff
from apps.fees.models import FeePayment, StudentFee
from apps.attendance.models import Attendance
from apps.courses.models import Course

try:
    from apps.leads.models import Lead
except ImportError:
    Lead = None


class SchoolAdminSite(AdminSite):
    site_header = "School Management System"
    site_title = "School Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        today = now().date()

        # 1. Total Counts
        extra_context["total_students"] = Student.objects.filter(is_active=True).count()
        extra_context["total_staff"] = Staff.objects.filter(is_active=True).count()
        extra_context["total_leads"] = Lead.objects.count() if Lead else 0
        extra_context["total_courses"] = Course.objects.filter(is_active=True).count()

        # 2. Financial Stats
        fees_collected = (
            FeePayment.objects.filter(is_active=True)
            .aggregate(total=Sum("amount"))["total"] or 0
        )
        total_expected = (
            StudentFee.objects.filter(is_active=True)
            .aggregate(total=Sum("final_fee"))["total"] or 0
        )
        
        extra_context["fees_collected"] = fees_collected
        extra_context["total_expected"] = total_expected
        extra_context["collection_rate"] = (
            round((fees_collected / total_expected) * 100, 2) if total_expected > 0 else 0
        )
        
        # Today's Collection
        extra_context["todays_collection"] = (
            FeePayment.objects.filter(is_active=True, created_at__date=today)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        # 3. Attendance Stats
        total_students = extra_context["total_students"]
        today_attendance = Attendance.objects.filter(date=today, status="present").count()
        extra_context["attendance_rate"] = (
            round((today_attendance / total_students) * 100, 2) if total_students > 0 else 0
        )

        # 4. Recent Data with Pagination
        payments_list = (
            FeePayment.objects.select_related("student_fee__student")
            .filter(is_active=True)
            .order_by("-created_at")
        )
        p_paginator = Paginator(payments_list, 10)
        p_page_number = request.GET.get("p_page")
        extra_context["recent_payments"] = p_paginator.get_page(p_page_number)

        # 5. Recent Activity with Pagination
        activity_list = (
            LogEntry.objects.select_related("user", "content_type")
            .order_by("-action_time")
        )
        a_paginator = Paginator(activity_list, 5)
        a_page_number = request.GET.get("a_page")
        extra_context["recent_activity"] = a_paginator.get_page(a_page_number)

        return super().index(request, extra_context)

    def get_urls(self):
        # Synchronize with default admin registry so all models are visible
        from django.contrib import admin
        for model, admin_class in admin.site._registry.items():
            try:
                self.register(model, admin_class.__class__)
            except admin.sites.AlreadyRegistered:
                pass
        return super().get_urls()


# 🔥 THIS LINE IS REQUIRED
school_admin_site = SchoolAdminSite(name="school_admin")
