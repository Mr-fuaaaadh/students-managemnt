from django.db import models
from common.models import TimeStampedModel, ActiveModel
from apps.courses.models import Course
from apps.staff.models import Staff


class LeadStatus(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    INTERESTED = "interested", "Interested"
    NOT_INTERESTED = "not_interested", "Not Interested"
    CONVERTED = "converted", "Converted"


class LeadSource(models.TextChoices):
    WALK_IN = "walk_in", "Walk-in"
    WEBSITE = "website", "Website"
    PHONE = "phone", "Phone Call"
    REFERRAL = "referral", "Referral"
    ADS = "ads", "Ads"


class Lead(TimeStampedModel, ActiveModel):
    name = models.CharField(max_length=150, db_index=True)
    phone = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(blank=True)

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        related_name="leads"
    )

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "sales"},
        related_name="assigned_leads"
    )

    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        db_index=True
    )

    source = models.CharField(
        max_length=20,
        choices=LeadSource.choices,
        default=LeadSource.WALK_IN
    )

    remarks = models.TextField(blank=True)

    converted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "is_active"]),
            models.Index(fields=["phone"]),
        ]
