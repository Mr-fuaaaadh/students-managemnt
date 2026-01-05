from django.db import models
from common.models import TimeStampedModel, ActiveModel


class Course(TimeStampedModel, ActiveModel):
    name = models.CharField(max_length=150, db_index=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    duration_months = models.PositiveIntegerField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name", "is_active"]),
        ]
