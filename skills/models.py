from django.contrib.auth.models import User
from django.db import models

CATEGORIES = [
    ("programming", "Programming"),
    ("design", "Graphic Design"),
    ("writing", "Content Writing"),
    ("tutoring", "Tutoring / Academic"),
    ("language", "Language"),
    ("video", "Video Editing"),
    ("marketing", "Marketing"),
    ("music", "Music & Arts"),
    ("other", "Other"),
]

LEVELS = [
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("advanced", "Advanced"),
    ("expert", "Expert"),
]


class Skill(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="other")
    level = models.CharField(max_length=15, choices=LEVELS, default="beginner")
    description = models.TextField(blank=True)
    open_for_exchange = models.BooleanField(
        default=True, help_text="Allow other students to request a skill exchange with you for this skill"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_level_display()}) - {self.owner.username}"
