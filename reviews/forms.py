from django import forms

from accounts.forms import StyledMixin

from .models import Review

RATING_CHOICES = [
    (5, "5 - Excellent"),
    (4, "4 - Very good"),
    (3, "3 - Good"),
    (2, "2 - Fair"),
    (1, "1 - Poor"),
]


class ReviewForm(StyledMixin, forms.ModelForm):
    rating = forms.TypedChoiceField(choices=RATING_CHOICES, coerce=int)

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {"comment": forms.Textarea(attrs={"rows": 4})}
