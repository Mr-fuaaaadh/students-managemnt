from django.db import models
from common.models import TimeStampedModel, ActiveModel
from apps.courses.models import Course


class Student(TimeStampedModel, ActiveModel):
    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, db_index=True)

    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="students"
    )
    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.course.name}) - {self.course.fees} INR"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        verbose_name_plural = "Students"
        ordering = ["first_name"]
        indexes = [
            models.Index(fields=["first_name", "phone"]),
            models.Index(fields=["course", "is_active"]),
        ]
