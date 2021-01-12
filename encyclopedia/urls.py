from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("randomPage", views.randomPage, name="random"),
    path("search", views.search, name="search"),
    path("<str:title>", views.title, name="title"),
    path("edit/<str:title>", views.edit, name="edit"),
    
]
