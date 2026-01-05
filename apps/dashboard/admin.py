from django.urls import path
from django.contrib import admin
from django.shortcuts import render
from django.db.models import Sum, F
from apps.staff.models import Staff
from apps.students.models import Student
from apps.fees.models import StudentFee, FeePayment

class DashboardAdmin(admin.AdminSite):
    site_header = "School Management Admin"
    site_title = "Admin Dashboard"
    index_title = "Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("dashboard/", self.admin_view(self.dashboard_view), name="dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        total_staff = Staff.objects.filter(is_active=True).count()
        total_students = Student.objects.filter(is_active=True).count()

        pending_fee = StudentFee.objects.annotate(
            paid=Sum(F('payments__amount'))
        ).aggregate(
            total_pending=Sum(F('final_fee') - F('paid'))
        )['total_pending'] or 0

        collected_fee = FeePayment.objects.aggregate(total_collected=Sum('amount'))['total_collected'] or 0

        context = {
            'total_staff': total_staff,
            'total_students': total_students,
            'pending_fee': pending_fee,
            'collected_fee': collected_fee,
        }
        return render(request, "dashboard/admin_dashboard.html", context)

# Replace the default admin site
admin_site = DashboardAdmin(name="myadmin")
