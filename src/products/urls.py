from django.contrib import admin  # NOQA: 401
from django.urls import path
from products.views import ProductInfo

app_name = "products"

urlpatterns = [
    path("info/<int:pk>/", ProductInfo.as_view(), name="product_info"),
]
