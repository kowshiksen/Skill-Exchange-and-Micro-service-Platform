from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import get_profile
from exchanges.models import ExchangeRequest
from services.models import ServiceOrder

from .forms import ReviewForm
from .models import Review


@login_required
def review_add_service(request, order_id):
    order = get_object_or_404(ServiceOrder, pk=order_id, buyer=request.user)
    if order.status != "completed":
        messages.error(request, "You can review a service only after it is completed.")
        return redirect("services:mine")
    if Review.objects.filter(order=order).exists():
        messages.warning(request, "You have already reviewed this.")
        return redirect("services:mine")

    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.reviewer = request.user
        review.reviewee = order.provider
        review.order = order
        review.save()
        messages.success(request, "Your review has been submitted. Thank you!")
        return redirect("services:mine")
    return render(
        request,
        "reviews/review_add.html",
        {"form": form, "target_user": order.provider, "subject": f"Service: {order.service.title}"},
    )


@login_required
def review_add_exchange(request, exchange_id):
    ex = get_object_or_404(ExchangeRequest, pk=exchange_id)
    if request.user not in (ex.requester, ex.receiver):
        messages.error(request, "You do not have permission to do that.")
        return redirect("exchanges:mine")
    if ex.status != "completed":
        messages.error(request, "You can review an exchange only after it is completed.")
        return redirect("exchanges:detail", pk=ex.pk)
    if Review.objects.filter(exchange=ex, reviewer=request.user).exists():
        messages.warning(request, "You have already reviewed this.")
        return redirect("exchanges:detail", pk=ex.pk)

    other = ex.receiver if ex.requester == request.user else ex.requester
    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.reviewer = request.user
        review.reviewee = other
        review.exchange = ex
        review.save()
        messages.success(request, "Your review has been submitted. Thank you!")
        return redirect("exchanges:detail", pk=ex.pk)
    return render(
        request,
        "reviews/review_add.html",
        {
            "form": form,
            "target_user": other,
            "subject": f"Skill exchange: {ex.offered_skill.name} / {ex.requested_skill.name}",
        },
    )


@login_required
def review_list(request, username=None):
    target = get_object_or_404(User, username=username) if username else request.user
    received = target.reviews_received.select_related("reviewer", "order__service", "exchange")
    given = (
        target.reviews_given.select_related("reviewee") if target == request.user else Review.objects.none()
    )
    return render(
        request,
        "reviews/review_list.html",
        {
            "target": target,
            "profile": get_profile(target),
            "received": received,
            "given": given,
            "is_me": target == request.user,
        },
    )
