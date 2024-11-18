from django.contrib import admin  # NOQA: 401
from django.urls import path

from shop.views import FavouritesView, IndexView

app_name = "shop"

urlpatterns = [
    path("favorites/", FavouritesView.as_view(), name="favorites_list"),
    path("", IndexView.as_view(), name="index"),
]
