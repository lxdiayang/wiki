from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("search", views.search, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random_entry", views.random_entry, name="random_entry")
]
