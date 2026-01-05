from django.utils import timezone
from django.db import transaction

from apps.students.models import Student
from .models import Lead, LeadStatus


@transaction.atomic
def convert_lead_to_student(lead: Lead) -> Student:
    """
    Converts a lead into a student safely.
    """

    if lead.status == LeadStatus.CONVERTED:
        raise ValueError("Lead already converted")

    if not lead.course:
        raise ValueError("Course is required to convert lead")

    # Prevent duplicate students (phone-based)
    existing_student = Student.objects.filter(phone=lead.phone).first()
    if existing_student:
        raise ValueError("Student with this phone already exists")

    # Split name safely
    name_parts = lead.name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    student = Student.objects.create(
        first_name=first_name,
        last_name=last_name,
        phone=lead.phone,
        email=lead.email or "",
        course=lead.course,
        is_active=True,
    )

    # Update lead
    lead.status = LeadStatus.CONVERTED
    lead.converted_at = timezone.now()
    lead.is_active = False
    lead.save(update_fields=["status", "converted_at", "is_active"])

    return student
