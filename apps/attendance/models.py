from django.db import models
from common.models import TimeStampedModel
from apps.students.models import Student


class Attendance(TimeStampedModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    date = models.DateField(db_index=True)

    STATUS_CHOICES = (
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("leave", "Leave"),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="present"
    )

    remark = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"
        unique_together = ("student", "date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["date", "status"]),
            models.Index(fields=["student", "date"]),
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"
