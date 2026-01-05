from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.students.models import Student
from apps.attendance.models import Attendance

class Command(BaseCommand):
    help = "Auto mark absent students after cutoff time"

    def handle(self, *args, **kwargs):
        today = now().date()

        # All active students
        students = Student.objects.filter(is_active=True)

        # Students who already have attendance today
        marked_students = Attendance.objects.filter(
            date=today
        ).values_list("student_id", flat=True)

        # Students without attendance today
        absent_students = students.exclude(id__in=marked_students)

        count = 0
        for student in absent_students:
            Attendance.objects.create(
                student=student,
                date=today,
                status="absent",
                remark="Auto marked absent"
            )
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Auto marked {count} students as ABSENT for {today}")
        )
