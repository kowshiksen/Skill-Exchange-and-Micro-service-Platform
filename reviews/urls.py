from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.review_list, name="list"),
    path("user/<str:username>/", views.review_list, name="user_list"),
    path("service/<int:order_id>/add/", views.review_add_service, name="add_service"),
    path("exchange/<int:exchange_id>/add/", views.review_add_exchange, name="add_exchange"),
]
