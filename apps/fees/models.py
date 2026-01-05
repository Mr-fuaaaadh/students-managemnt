from django.db import models
from common.models import TimeStampedModel, ActiveModel
from apps.students.models import Student
from apps.staff.models import Staff


class FeeStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PARTIAL = "partial", "Partial"
    PAID = "paid", "Paid"


class StudentFee(TimeStampedModel, ActiveModel):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="fee_account"
    )

    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_fee = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=FeeStatus.choices,
        default=FeeStatus.PENDING,
        db_index=True
    )

    def __str__(self):
        return f"{self.student.full_name} - ₹{self.final_fee}"

    @property
    def paid_amount(self):
        return sum(
            p.amount for p in self.payments.filter(is_active=True)
        )

    @property
    def due_amount(self):
        return self.final_fee - self.paid_amount

    # 🔥 AUTO STATUS LOGIC
    def update_status(self):
        paid = self.paid_amount

        if paid <= 0:
            self.status = FeeStatus.PENDING
        elif paid < self.final_fee:
            self.status = FeeStatus.PARTIAL
        else:
            self.status = FeeStatus.PAID

        self.save(update_fields=["status"])

    class Meta:
        verbose_name = "Student Fee"
        verbose_name_plural = "Student Fees"
        indexes = [
            models.Index(fields=["status", "is_active"]),
        ]


class FeePayment(TimeStampedModel, ActiveModel):
    student_fee = models.ForeignKey(
        StudentFee,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    collected_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "accounts"}
    )

    reference_no = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student_fee.student.full_name} - ₹{self.amount}"

    class Meta:
        verbose_name = "Fee Payment"
        verbose_name_plural = "Fee Payments"
        ordering = ["-payment_date"]




class LedgerType(models.TextChoices):
    DEBIT = "debit", "Debit"
    CREDIT = "credit", "Credit"


class FeeLedger(TimeStampedModel, ActiveModel):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="fee_ledger"
    )

    student_fee = models.ForeignKey(
        StudentFee,
        on_delete=models.CASCADE,
        related_name="ledger_entries"
    )

    payment = models.ForeignKey(
        FeePayment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ledger_entries"
    )

    entry_type = models.CharField(
        max_length=10,
        choices=LedgerType.choices,
        db_index=True
    )

    description = models.CharField(max_length=255)

    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["student", "created_at"]),
        ]

    def __str__(self):
        return f"{self.student.full_name} | {self.entry_type} | Bal: {self.balance}"
