from django.contrib import admin

from .models import ExchangeRequest


@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = ("requester", "receiver", "offered_skill", "requested_skill", "status", "created_at")
    list_filter = ("status",)
