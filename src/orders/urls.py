from django.contrib import admin  # NOQA: 401
from django.urls import path

from orders.views import OrderDetailView

app_name = "orders"

urlpatterns = [
    path("", OrderDetailView.as_view(), name="detail"),
]
