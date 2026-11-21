from django.contrib import admin

from .models import Service, ServiceOrder


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "provider", "category", "price", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("title", "provider__username")


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "buyer", "provider", "price", "status", "created_at")
    list_filter = ("status",)
