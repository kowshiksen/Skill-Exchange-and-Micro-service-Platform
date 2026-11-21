from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from reviews.models import Review
from skills.models import CATEGORIES

from .forms import OrderForm, ServiceForm
from .models import Service, ServiceOrder


@login_required
def service_list(request):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    sort = request.GET.get("sort", "new")
    services = Service.objects.filter(is_active=True).select_related("provider", "provider__profile")
    if q:
        services = services.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        services = services.filter(category=category)
    if sort == "low":
        services = services.order_by("price")
    elif sort == "high":
        services = services.order_by("-price")
    return render(
        request,
        "services/service_list.html",
        {"services": services, "q": q, "category": category, "sort": sort, "categories": CATEGORIES},
    )


@login_required
def service_add(request):
    form = ServiceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        service = form.save(commit=False)
        service.provider = request.user
        service.save()
        messages.success(request, "Service published successfully.")
        return redirect("services:mine")
    return render(request, "services/service_add.html", {"form": form})


@login_required
def service_detail(request, pk):
    service = get_object_or_404(Service.objects.select_related("provider", "provider__profile"), pk=pk)
    is_owner = service.provider == request.user
    if not service.is_active and not is_owner:
        raise Http404
    reviews = Review.objects.filter(order__service=service).select_related("reviewer")
    return render(
        request,
        "services/service_detail.html",
        {"service": service, "is_owner": is_owner, "reviews": reviews},
    )


@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Service updated successfully.")
        return redirect("services:mine")
    return render(request, "services/service_edit.html", {"form": form, "service": service})


@login_required
@require_POST
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user)
    service.delete()
    messages.success(request, "Service deleted successfully.")
    return redirect("services:mine")


@login_required
def service_order(request, service_id):
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    if service.provider == request.user:
        messages.error(request, "You cannot order your own service.")
        return redirect("services:detail", pk=service.pk)
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save(commit=False)
        order.service = service
        order.buyer = request.user
        order.provider = service.provider
        order.price = service.price
        order.save()
        messages.success(request, "Your order request has been sent. You can pay once the provider accepts it.")
        return redirect("services:mine")
    return render(request, "services/service_order.html", {"form": form, "service": service})


@login_required
def my_services(request):
    user = request.user
    context = {
        "services": user.services.all(),
        "received_orders": user.received_orders.select_related("service", "buyer"),
        "sent_orders": user.service_orders.select_related("service", "provider"),
    }
    return render(request, "services/my_services.html", context)


@login_required
@require_POST
def order_action(request, pk, action):
    order = get_object_or_404(ServiceOrder, pk=pk)
    user = request.user
    new_status = None

    if action in ("accept", "reject") and order.provider == user and order.status == "pending":
        new_status = "accepted" if action == "accept" else "rejected"
    elif action == "cancel" and order.buyer == user and order.status in ("pending", "accepted"):
        new_status = "cancelled"
    elif action == "complete" and order.provider == user and order.status == "paid":
        new_status = "completed"

    if new_status is None:
        messages.error(request, "This action is not available right now.")
    else:
        order.status = new_status
        order.save()
        messages.success(request, f"Order status: {order.get_status_display()}")
    return redirect("services:mine")
