from django.utils.timezone import now
from django.db.models import Sum

from apps.students.models import Student
from apps.staff.models import Staff
from apps.teachers.models import Teacher
from apps.attendance.models import Attendance
from apps.fees.models import FeePayment


def kpi_cards(request):
    today = now().date()

    present_count = Attendance.objects.filter(
        date=today,
        status="present"
    ).count()

    absent_count = Attendance.objects.filter(
        date=today,
        status="absent"
    ).count()

    total_fees = FeePayment.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return [
        {
            "title": "Students",
            "metric": Student.objects.count(),
            "icon": "person",
            "color": "blue",
        },
        {
            "title": "Staff",
            "metric": Staff.objects.count(),
            "icon": "group",
            "color": "green",
        },
        {
            "title": "Teachers",
            "metric": Teacher.objects.count(),
            "icon": "school",
            "color": "purple",
        },
        {
            "title": "Today Present",
            "metric": present_count,
            "icon": "check_circle",
            "color": "emerald",
        },
        {
            "title": "Today Absent",
            "metric": absent_count,
            "icon": "cancel",
            "color": "red",
        },
        {
            "title": "Total Fees",
            "metric": f"₹ {total_fees}",
            "icon": "payments",
            "color": "amber",
        },
    ]
