from django.contrib import admin  # NOQA: 401
from django.urls import path

from orders.views import OrderCheckoutView, OrderDetailView

app_name = "orders"

urlpatterns = [
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("checkout", OrderCheckoutView.as_view(), name="checkout"),
]
