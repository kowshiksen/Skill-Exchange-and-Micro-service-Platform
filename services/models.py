from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from skills.models import CATEGORIES


class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(1)],
        help_text="BDT (taka)",
    )
    delivery_days = models.PositiveSmallIntegerField(default=3, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.price} BDT"


class ServiceOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted (payment due)"),
        ("rejected", "Rejected"),
        ("paid", "Paid (in progress)"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="orders")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_orders")
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_orders")
    message = models.TextField(help_text="Describe what you need")
    price = models.DecimalField(max_digits=8, decimal_places=2)  # price at the time of ordering
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}: {self.service.title} ({self.status})"
