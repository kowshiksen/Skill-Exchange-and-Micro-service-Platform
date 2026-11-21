import uuid

from django.contrib.auth.models import User
from django.db import models


def generate_txn_id():
    return "TXN" + uuid.uuid4().hex[:12].upper()


class Transaction(models.Model):
    """DEMO payment only - no real payment gateway is used."""

    METHODS = [
        ("bkash", "bKash "),
        ("nagad", "Nagad "),
        ("rocket", "Rocket "),
        ("card", "Card "),
    ]
    STATUS_CHOICES = [("success", "Success"), ("failed", "Failed")]

    order = models.OneToOneField(
        "services.ServiceOrder", on_delete=models.CASCADE, related_name="transaction"
    )
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_made")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_received")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=10, choices=METHODS, default="bkash")
    transaction_id = models.CharField(max_length=20, unique=True, default=generate_txn_id)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="success")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_id} - {self.amount} BDT"
