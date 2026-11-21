from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from reviews.models import Review
from skills.models import CATEGORIES, Skill

from .forms import ExchangeRequestForm
from .models import ExchangeRequest


@login_required
def exchange_list(request):
    """Skills that are open for exchange (excluding the current user's own skills)."""
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    skills = (
        Skill.objects.filter(open_for_exchange=True)
        .exclude(owner=request.user)
        .select_related("owner", "owner__profile")
    )
    if q:
        skills = skills.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category:
        skills = skills.filter(category=category)
    return render(
        request,
        "exchanges/exchange_list.html",
        {"skills": skills, "q": q, "category": category, "categories": CATEGORIES},
    )


@login_required
def exchange_add(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id, open_for_exchange=True)
    if skill.owner == request.user:
        messages.error(request, "You cannot request an exchange for your own skill.")
        return redirect("skills:detail", pk=skill.pk)
    if not request.user.skills.exists():
        messages.warning(request, "Please add at least one of your own skills before requesting an exchange.")
        return redirect("skills:add")
    if ExchangeRequest.objects.filter(
        requester=request.user, requested_skill=skill, status="pending"
    ).exists():
        messages.warning(request, "You already have a pending request for this skill.")
        return redirect("exchanges:mine")

    form = ExchangeRequestForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        ex = form.save(commit=False)
        ex.requester = request.user
        ex.receiver = skill.owner
        ex.requested_skill = skill
        ex.save()
        messages.success(request, "Exchange request sent successfully.")
        return redirect("exchanges:mine")
    return render(request, "exchanges/exchange_add.html", {"form": form, "skill": skill})


@login_required
def exchange_detail(request, pk):
    ex = get_object_or_404(
        ExchangeRequest.objects.select_related(
            "requester", "receiver", "requested_skill", "offered_skill"
        ),
        pk=pk,
    )
    if request.user not in (ex.requester, ex.receiver):
        messages.error(request, "You do not have permission to view this exchange.")
        return redirect("exchanges:mine")
    can_review = (
        ex.status == "completed"
        and not Review.objects.filter(exchange=ex, reviewer=request.user).exists()
    )
    return render(
        request,
        "exchanges/exchange_detail.html",
        {
            "ex": ex,
            "is_receiver": ex.receiver == request.user,
            "is_requester": ex.requester == request.user,
            "can_review": can_review,
            "other_user": ex.receiver if ex.requester == request.user else ex.requester,
        },
    )


@login_required
def exchange_requests(request):
    """Requests received by the current user."""
    received = request.user.received_exchanges.select_related(
        "requester", "requested_skill", "offered_skill"
    )
    return render(request, "exchanges/exchange_requests.html", {"requests": received})


@login_required
def my_exchanges(request):
    """Requests sent by the current user."""
    sent = request.user.sent_exchanges.select_related(
        "receiver", "requested_skill", "offered_skill"
    )
    return render(request, "exchanges/my_exchanges.html", {"requests": sent})


@login_required
@require_POST
def exchange_action(request, pk, action):
    ex = get_object_or_404(ExchangeRequest, pk=pk)
    user = request.user
    new_status = None

    if action in ("accept", "reject") and ex.receiver == user and ex.status == "pending":
        new_status = "accepted" if action == "accept" else "rejected"
    elif action == "cancel" and ex.requester == user and ex.status == "pending":
        new_status = "cancelled"
    elif action == "complete" and user in (ex.requester, ex.receiver) and ex.status == "accepted":
        new_status = "completed"

    if new_status is None:
        messages.error(request, "This action is not available right now.")
    else:
        ex.status = new_status
        ex.save()
        messages.success(request, f"Exchange status: {ex.get_status_display()}")
    return redirect("exchanges:detail", pk=ex.pk)
