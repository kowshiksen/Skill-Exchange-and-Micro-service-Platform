from django import forms

from accounts.forms import StyledMixin

from .models import Skill


class SkillForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category", "level", "description", "open_for_exchange"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
