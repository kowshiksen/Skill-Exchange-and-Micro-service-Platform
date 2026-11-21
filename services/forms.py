from django import forms

from accounts.forms import StyledMixin

from .models import Service, ServiceOrder


class ServiceForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "category", "description", "price", "delivery_days", "is_active"]
        labels = {"price": "Price (BDT)", "is_active": "This service is currently available"}
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}


class OrderForm(StyledMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ["message"]
        labels = {"message": "Your requirement"}
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
