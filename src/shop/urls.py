from django.contrib import admin  # NOQA: 401
from django.urls import path

from shop.views import (FavouritesView, IndexView, product_generator,
                        reviews_generator)

app_name = "shop"

urlpatterns = [
    path("favorites/", FavouritesView.as_view(), name="favorites_list"),
    path("", IndexView.as_view(), name="index"),
    path("product-generator/", product_generator, name="product-generator"),
    path("review-generator/", reviews_generator, name="reviews_generator"),
    path("customer-generator/", reviews_generator, name="customer_generator"),
]
