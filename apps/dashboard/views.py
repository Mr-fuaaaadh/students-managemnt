from django.shortcuts import render
from django.utils.timezone import now
from apps.students.models import Student
from apps.staff.models import Staff
from apps.fees.models import FeePayment
from apps.attendance.models import Attendance
from django.db.models import Sum

def admin_dashboard(request):
    today = now().date()

    context = {
        "total_students": Student.objects.filter(is_active=True).count(),
        "total_staff": Staff.objects.filter(is_active=True).count(),
        "total_fees": FeePayment.objects.aggregate(total=Sum("amount"))["total"] or 0,
        "today_attendance": Attendance.objects.filter(date=today).count(),
    }
    return render(request, "admin/admin_dashboard.html", context)
