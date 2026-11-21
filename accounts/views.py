
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileForm, RegisterForm, UserUpdateForm
from .models import DEPARTMENTS, Profile, get_profile



def register(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        messages.success(
            request,
            "Registration successful! Please login with your account."
        )

        # Redirect to Login Page instead of Dashboard
        return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})


# User Profile
@login_required
def profile(request, username=None):
    profile_user = (
        get_object_or_404(User, username=username)
        if username
        else request.user
    )

    prof = get_profile(profile_user)

    context = {
        "profile_user": profile_user,
        "profile": prof,
        "skills": profile_user.skills.all(),
        "services": profile_user.services.filter(is_active=True),
        "reviews": profile_user.reviews_received.select_related("reviewer")[:5],
        "is_me": profile_user == request.user,
    }

    return render(request, "accounts/profile.html", context)


# Edit User Profile
@login_required
def edit_profile(request):
    prof = get_profile(request.user)

    user_form = UserUpdateForm(
        request.POST or None,
        instance=request.user
    )

    profile_form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=prof
    )

    if (
        request.method == "POST"
        and user_form.is_valid()
        and profile_form.is_valid()
    ):
        user_form.save()
        profile_form.save()

        messages.success(request, "Profile updated successfully.")

        return redirect("accounts:profile")

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


# Student Search
@login_required
def student_search(request):
    q = request.GET.get("q", "").strip()
    dept = request.GET.get("department", "")

    profiles = Profile.objects.select_related("user").order_by(
        "user__first_name"
    )

    if q:
        profiles = profiles.filter(
            Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(student_id__icontains=q)
            | Q(user__skills__name__icontains=q)
        ).distinct()

    if dept:
        profiles = profiles.filter(department=dept)

    return render(
        request,
        "accounts/student_search.html",
        {
            "profiles": profiles,
            "q": q,
            "dept": dept,
            "departments": DEPARTMENTS,
        },
    )
