from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import transaction

from .models import DEPARTMENTS, Profile


class StyledMixin:
    """Adds CSS classes to every form field (also imported by other apps)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check")
            else:
                field.widget.attrs.setdefault("class", "form-control")


class LoginForm(StyledMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Student ID"


class RegisterForm(StyledMixin, forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    student_id = forms.CharField(
        max_length=20,
        label="Student ID",
        help_text="This will be your login username.",
        validators=[RegexValidator(r"^[\w.@+-]+$", "Spaces and special characters are not allowed.")],
    )
    email = forms.EmailField()
    department = forms.ChoiceField(choices=DEPARTMENTS)
    phone = forms.CharField(max_length=20, required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    def clean_student_id(self):
        sid = self.cleaned_data["student_id"].strip()
        if User.objects.filter(username__iexact=sid).exists():
            raise ValidationError("An account with this Student ID already exists.")
        return sid

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean(self):
        data = super().clean()
        p1, p2 = data.get("password1"), data.get("password2")
        if p1 and p2:
            if p1 != p2:
                self.add_error("password2", "The two passwords do not match.")
            else:
                try:
                    validate_password(p1)
                except ValidationError as e:
                    self.add_error("password1", e)
        return data

    @transaction.atomic
    def save(self):
        d = self.cleaned_data
        user = User.objects.create_user(
            username=d["student_id"],
            email=d["email"],
            password=d["password1"],
            first_name=d["first_name"],
            last_name=d["last_name"],
        )
        Profile.objects.create(
            user=user,
            student_id=d["student_id"],
            department=d["department"],
            phone=d["phone"],
        )
        return user


class UserUpdateForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["department", "phone", "bio", "photo"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}
