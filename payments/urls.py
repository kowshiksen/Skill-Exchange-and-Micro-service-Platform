from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("history/", views.payment_history, name="history"),
    path("pay/<int:order_id>/", views.payment, name="pay"),
]
