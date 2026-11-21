from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SkillForm
from .models import CATEGORIES, LEVELS, Skill


@login_required
def skill_list(request):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    level = request.GET.get("level", "")
    skills = Skill.objects.select_related("owner", "owner__profile")
    if q:
        skills = skills.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(owner__first_name__icontains=q)
        )
    if category:
        skills = skills.filter(category=category)
    if level:
        skills = skills.filter(level=level)
    return render(
        request,
        "skills/skill_list.html",
        {"skills": skills, "q": q, "category": category, "level": level,
         "categories": CATEGORIES, "levels": LEVELS},
    )


@login_required
def skill_add(request):
    form = SkillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        skill = form.save(commit=False)
        skill.owner = request.user
        skill.save()
        messages.success(request, "Skill added successfully.")
        return redirect("skills:mine")
    return render(request, "skills/skill_add.html", {"form": form})


@login_required
def skill_detail(request, pk):
    skill = get_object_or_404(Skill.objects.select_related("owner", "owner__profile"), pk=pk)
    is_owner = skill.owner == request.user
    return render(
        request,
        "skills/skill_detail.html",
        {"skill": skill, "is_owner": is_owner,
         "can_exchange": skill.open_for_exchange and not is_owner},
    )


@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk, owner=request.user)
    form = SkillForm(request.POST or None, instance=skill)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill updated successfully.")
        return redirect("skills:mine")
    return render(request, "skills/skill_edit.html", {"form": form, "skill": skill})


@login_required
@require_POST
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk, owner=request.user)
    skill.delete()
    messages.success(request, "Skill deleted successfully.")
    return redirect("skills:mine")


@login_required
def my_skills(request):
    return render(request, "skills/my_skills.html", {"skills": request.user.skills.all()})
