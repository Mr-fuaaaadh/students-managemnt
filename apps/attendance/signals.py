from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from apps.students.models import Student
from .models import Attendance


@receiver(post_save, sender=Student)
def create_today_attendance(sender, instance, created, **kwargs):
    if created:
        Attendance.objects.create(
            student=instance,
            date=now().date(),
            status="present"
        )
