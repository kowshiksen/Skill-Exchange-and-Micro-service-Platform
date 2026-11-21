from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("", views.service_list, name="list"),
    path("add/", views.service_add, name="add"),
    path("mine/", views.my_services, name="mine"),
    path("<int:pk>/", views.service_detail, name="detail"),
    path("<int:pk>/edit/", views.service_edit, name="edit"),
    path("<int:pk>/delete/", views.service_delete, name="delete"),
    path("<int:service_id>/order/", views.service_order, name="order"),
    path("order/<int:pk>/<str:action>/", views.order_action, name="order_action"),
]
