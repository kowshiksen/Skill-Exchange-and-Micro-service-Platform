from django.urls import path

from . import views

app_name = "exchanges"

urlpatterns = [
    path("", views.exchange_list, name="list"),
    path("request/<int:skill_id>/", views.exchange_add, name="add"),
    path("received/", views.exchange_requests, name="requests"),
    path("sent/", views.my_exchanges, name="mine"),
    path("<int:pk>/", views.exchange_detail, name="detail"),
    path("<int:pk>/<str:action>/", views.exchange_action, name="action"),
]
