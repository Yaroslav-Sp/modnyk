from django.contrib import admin  # NOQA: 401
from django.urls import path

from accounts.views import CustomerProfile

app_name = "customer"

urlpatterns = [
    path("", CustomerProfile.as_view(), name="profile"),
]
