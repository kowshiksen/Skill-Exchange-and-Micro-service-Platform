from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "category", "level", "open_for_exchange", "created_at")
    list_filter = ("category", "level", "open_for_exchange")
    search_fields = ("name", "owner__username")
