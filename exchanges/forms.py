from django import forms

from accounts.forms import StyledMixin

from .models import ExchangeRequest


class ExchangeRequestForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ["offered_skill", "message"]
        labels = {"offered_skill": "Which skill will you offer?"}
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["offered_skill"].queryset = user.skills.all()
        self.fields["offered_skill"].empty_label = None
