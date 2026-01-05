from django.db import models
from django.contrib.auth.models import AbstractUser

from common.models import TimeStampedModel, ActiveModel


class StaffRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    TEACHER = "teacher", "Teacher"
    SALES = "sales", "Sales"
    ACCOUNTS = "accounts", "Accounts"


class Staff(AbstractUser, TimeStampedModel, ActiveModel):
    """
    Custom User model for staff.
    """
    role = models.CharField(max_length=20, choices=StaffRole.choices, db_index=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        indexes = [
            models.Index(fields=["role", "is_active"]),
        ]
