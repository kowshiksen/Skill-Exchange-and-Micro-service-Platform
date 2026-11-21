from django.urls import path

from . import views

app_name = "skills"

urlpatterns = [
    path("", views.skill_list, name="list"),
    path("add/", views.skill_add, name="add"),
    path("mine/", views.my_skills, name="mine"),
    path("<int:pk>/", views.skill_detail, name="detail"),
    path("<int:pk>/edit/", views.skill_edit, name="edit"),
    path("<int:pk>/delete/", views.skill_delete, name="delete"),
]
