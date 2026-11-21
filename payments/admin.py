from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "payer", "receiver", "amount", "method", "status", "created_at")
    list_filter = ("method", "status")
