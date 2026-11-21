from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

DEPARTMENTS = [
    ("CSE", "Computer Science & Engineering"),
    ("EEE", "Electrical & Electronic Engineering"),
    ("CE", "Civil Engineering"),
    ("BBA", "Business Administration"),
    ("ENG", "English"),
    ("LAW", "Law"),
    ("OTH", "Other"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=10, choices=DEPARTMENTS, default="OTH")
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.student_id})"

    @property
    def average_rating(self):
        from reviews.models import Review

        avg = Review.objects.filter(reviewee=self.user).aggregate(a=Avg("rating"))["a"]
        return round(avg, 1) if avg else None

    @property
    def review_count(self):
        from reviews.models import Review

        return Review.objects.filter(reviewee=self.user).count()


def get_profile(user):
    """Create a profile automatically if the user (e.g. a superuser) does not have one."""
    profile, _ = Profile.objects.get_or_create(
        user=user, defaults={"student_id": user.username[:20], "department": "OTH"}
    )
    return profile
