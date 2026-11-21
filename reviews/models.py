from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    # A review belongs either to a service order or to a skill exchange
    order = models.OneToOneField(
        "services.ServiceOrder", on_delete=models.CASCADE, null=True, blank=True, related_name="review"
    )
    exchange = models.ForeignKey(
        "exchanges.ExchangeRequest", on_delete=models.CASCADE, null=True, blank=True,
        related_name="reviews",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["exchange", "reviewer"], name="unique_exchange_review")
        ]

    def __str__(self):
        return f"{self.reviewer.username} -> {self.reviewee.username}: {self.rating}/5"

    @property
    def stars(self):
        return "★" * self.rating + "☆" * (5 - self.rating)
