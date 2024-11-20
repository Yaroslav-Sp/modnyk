from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from api.serializers import (CustomerSerializer, OrderItemChangeSerializer,
                             OrderSerializer, ProductChangeSerializer,
                             ProductSerializer)
from orders.models import Order, OrderItem
from products.models import Product


# accounts_api_views
class CustomerViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


# products_api_views
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        return Product.objects.get(category__pk=self.kwargs.get("category_pk"), pk=self.kwargs.get("product_pk"))


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCreateView(CreateAPIView):
    serializer_class = ProductChangeSerializer
    queryset = Product.objects.all()


class ProductDeleteView(DestroyAPIView):
    serializer_class = ProductChangeSerializer

    def get_object(self):
        return Product.objects.get(pk=self.kwargs["pk"])


class ProductUpdateView(UpdateAPIView):
    serializer_class = ProductChangeSerializer

    def get_object(self):
        return Product.objects.get(pk=self.kwargs["pk"])


# orders_api_views


class OrdersListView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrdersDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        return Order.objects.get(pk=self.kwargs.get("pk"))


class OrderItemCreateView(CreateAPIView):
    serializer_class = OrderItemChangeSerializer

    def perform_create(self, serializer):
        serializer.save(order_id=self.kwargs.get("pk"))

    def get_object(self):
        return OrderItem.objects.get(
            order__pk=self.kwargs.get("pk"),
        )


class OrderItemDeleteView(DestroyAPIView):
    serializer_class = OrderItemChangeSerializer

    def perform_create(self, serializer):
        serializer.save(order_id=self.kwargs.get("pk"))

    def get_object(self):
        return OrderItem.objects.get(order__pk=self.kwargs.get("order_pk"), pk=self.kwargs.get("order_item_pk"))


class OrderItemUpdateView(UpdateAPIView):
    serializer_class = OrderItemChangeSerializer

    def get_object(self):
        return OrderItem.objects.get(order__pk=self.kwargs.get("order_pk"), pk=self.kwargs.get("order_item_pk"))
