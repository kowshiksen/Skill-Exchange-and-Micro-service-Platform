from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from services.models import ServiceOrder

from .models import Transaction


@login_required
def payment(request, order_id):
    order = get_object_or_404(
        ServiceOrder.objects.select_related("service", "provider"),
        pk=order_id,
        buyer=request.user,
    )
    if order.status != "accepted":
        messages.error(request, "This order cannot be paid for right now.")
        return redirect("services:mine")

    if request.method == "POST":
        method = request.POST.get("method")
        if method not in dict(Transaction.METHODS):
            messages.error(request, "Please select a payment method.")
        else:
            with db_transaction.atomic():
                Transaction.objects.create(
                    order=order,
                    payer=request.user,
                    receiver=order.provider,
                    amount=order.price,
                    method=method,
                    status="success",
                )
                order.status = "paid"
                order.save()
            messages.success(request, "Demo payment successful!")
            return redirect("payments:history")

    return render(
        request,
        "payments/payment.html",
        {"order": order, "methods": Transaction.METHODS},
    )


@login_required
def payment_history(request):
    user = request.user
    transactions = Transaction.objects.filter(Q(payer=user) | Q(receiver=user)).select_related(
        "order__service", "payer", "receiver"
    )
    spent = Transaction.objects.filter(payer=user, status="success").aggregate(t=Sum("amount"))["t"] or 0
    earned = (
        Transaction.objects.filter(receiver=user, status="success").aggregate(t=Sum("amount"))["t"] or 0
    )
    return render(
        request,
        "payments/payment_history.html",
        {"transactions": transactions, "spent": spent, "earned": earned},
    )
