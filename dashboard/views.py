from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render

from accounts.models import Profile, get_profile
from exchanges.models import ExchangeRequest
from payments.models import Transaction
from services.models import Service, ServiceOrder
from skills.models import Skill


def home(request):
    completed = (
        ServiceOrder.objects.filter(status="completed").count()
        + ExchangeRequest.objects.filter(status="completed").count()
    )
    context = {
        "total_students": Profile.objects.count(),
        "total_skills": Skill.objects.count(),
        "total_services": Service.objects.filter(is_active=True).count(),
        "total_completed": completed,
        "latest_services": Service.objects.filter(is_active=True).select_related("provider")[:6],
        "latest_skills": Skill.objects.filter(open_for_exchange=True).select_related("owner")[:6],
    }
    return render(request, "home.html", context)


@login_required
def dashboard(request):
    user = request.user
    profile = get_profile(user)

    received_ex = user.received_exchanges.select_related("requester", "requested_skill", "offered_skill")
    sent_ex = user.sent_exchanges.select_related("receiver", "requested_skill", "offered_skill")
    received_orders = user.received_orders.select_related("service", "buyer")
    sent_orders = user.service_orders.select_related("service", "provider")

    earned = Transaction.objects.filter(receiver=user, status="success").aggregate(t=Sum("amount"))["t"] or 0
    spent = Transaction.objects.filter(payer=user, status="success").aggregate(t=Sum("amount"))["t"] or 0

    context = {
        "profile": profile,
        "skills": user.skills.all()[:5],
        "skill_count": user.skills.count(),
        "services": user.services.all()[:5],
        "service_count": user.services.count(),
        "received_ex": received_ex[:5],
        "sent_ex": sent_ex[:5],
        "pending_received_ex": received_ex.filter(status="pending").count(),
        "active_exchanges": (
            received_ex.filter(status="accepted").count() + sent_ex.filter(status="accepted").count()
        ),
        "completed_exchanges": (
            received_ex.filter(status="completed").count() + sent_ex.filter(status="completed").count()
        ),
        "received_orders": received_orders[:5],
        "sent_orders": sent_orders[:5],
        "pending_received_orders": received_orders.filter(status="pending").count(),
        "earned": earned,
        "spent": spent,
        "recent_transactions": Transaction.objects.filter(Q(payer=user) | Q(receiver=user))
        .select_related("order__service", "payer", "receiver")[:5],
    }
    return render(request, "dashboard/dashboard.html", context)
