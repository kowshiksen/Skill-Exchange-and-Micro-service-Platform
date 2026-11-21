from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("student_id", "user", "department", "phone", "created_at")
    search_fields = ("student_id", "user__first_name", "user__last_name")
    list_filter = ("department",)
