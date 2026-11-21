from django.contrib.auth.models import User
from django.db import models


class ExchangeRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_exchanges")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_exchanges")
    requested_skill = models.ForeignKey(
        "skills.Skill", on_delete=models.CASCADE, related_name="incoming_exchanges"
    )
    offered_skill = models.ForeignKey(
        "skills.Skill", on_delete=models.CASCADE, related_name="outgoing_exchanges"
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.requester.username} <-> {self.receiver.username}: {self.offered_skill.name} / {self.requested_skill.name}"
