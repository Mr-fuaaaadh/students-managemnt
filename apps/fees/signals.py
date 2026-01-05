from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FeePayment, StudentFee, FeeLedger, LedgerType, FeeStatus

# -----------------------------
# Helper: Get last balance for ledger
# -----------------------------
def get_last_balance(student):
    last = FeeLedger.objects.filter(student=student).order_by("-created_at").first()
    return last.balance if last else 0


# -----------------------------
# Signal: Create ledger when StudentFee is created
# -----------------------------
@receiver(post_save, sender=StudentFee)
def create_fee_ledger(sender, instance, created, **kwargs):
    if created:
        balance = get_last_balance(instance.student) + instance.final_fee

        FeeLedger.objects.create(
            student=instance.student,
            student_fee=instance,
            entry_type=LedgerType.DEBIT,
            description="Total Fee Added",
            debit=instance.final_fee,
            credit=0,
            balance=balance,
        )


# -----------------------------
# Signal: Update StudentFee status and create ledger for payments
# -----------------------------
@receiver([post_save, post_delete], sender=FeePayment)
def update_fee_payment(sender, instance, **kwargs):
    fee = instance.student_fee

    # --- Update StudentFee status ---
    fee.update_status()

    # --- Create ledger entry only on new payments ---
    if sender == FeePayment and kwargs.get('created', False):
        balance = get_last_balance(fee.student) - instance.amount

        FeeLedger.objects.create(
            student=fee.student,
            student_fee=fee,
            payment=instance,
            entry_type=LedgerType.CREDIT,
            description="Fee Payment Received",
            debit=0,
            credit=instance.amount,
            balance=balance,
        )
