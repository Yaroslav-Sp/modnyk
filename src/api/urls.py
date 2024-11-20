from django.urls import include, path
from rest_framework import routers

from api.views import (CustomerViewSet, OrderItemCreateView,
                       OrderItemDeleteView, OrderItemUpdateView,
                       OrdersDetailView, OrdersListView, ProductCreateView,
                       ProductDeleteView, ProductDetailView, ProductListView,
                       ProductUpdateView)

customer_router = routers.DefaultRouter()
customer_router.register("customer", CustomerViewSet)


app_name = "api"

urlpatterns = [
    path("", include(customer_router.urls)),
    path("category/<int:category_pk>/products/<int:product_pk>/", ProductDetailView.as_view(), name="product_details"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("create-product/", ProductCreateView.as_view(), name="create_product"),
    path("delete-product/<int:pk>/", ProductDeleteView.as_view(), name="delete_product"),
    path("update-product/<int:pk>/", ProductUpdateView.as_view(), name="update_product"),
    path("update-product/<int:pk>/", ProductUpdateView.as_view(), name="update_product"),
    path("order/<int:pk>/", OrdersDetailView.as_view(), name="order_details"),
    path("orders/", OrdersListView.as_view(), name="order_list"),
    path("order/<int:pk>/order-item-create/", OrderItemCreateView.as_view(), name="order_item_create"),
    path(
        "order/<int:order_pk>/order-item-delete/<int:order_item_pk>/",
        OrderItemDeleteView.as_view(),
        name="order_item_delete",
    ),
    path(
        "order/<int:order_pk>/order-item-update/<int:order_item_pk>/",
        OrderItemUpdateView.as_view(),
        name="order_item_update",
    ),
]
