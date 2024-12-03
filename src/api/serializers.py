from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from orders.models import DeliveryAddress, Order, OrderItem, Payment
from products.models import Brand, Category, Color, Product, Size

# accounts_serializers


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "is_staff"]


# products_serializers


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = ["name", "description"]


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ["name"]


class CategorySerializer(ModelSerializer):
    level = CharField(source="get_level_display")
    parent = CharField(source="parent.name", read_only=True)

    class Meta:
        model = Category
        fields = ["name", "parent", "level"]


class ProductSerializer(ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    color = ColorSerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    size = SizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "description", "category", "color", "size", "price", "brand"]


class ProductChangeSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "color", "size", "price", "brand"]


# orders_serializers
class OrderItemSerializer(ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity"]


class OrderItemChangeSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity"]


class PaymentSerializer(ModelSerializer):
    status = CharField(source="get_status_display")
    payment_method = CharField(source="get_payment_method_display")

    class Meta:
        model = Payment
        fields = ["id", "amount", "payment_method", "status"]


class DeliveryAddressSerializer(ModelSerializer):
    customer = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = DeliveryAddress
        fields = ["id", "customer", "street_address", "city", "state", "postal_code", "country"]


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer(many=False, read_only=True)
    status = CharField(source="get_status_display")
    delivery_type = CharField(source="get_delivery_type_display")
    delivery_address = DeliveryAddressSerializer(many=False, read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    order_payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "status",
            "total_amount",
            "delivery_address",
            "recipients_first_name",
            "recipients_last_name",
            "recipients_phone_number",
            "delivery_type",
            "order_items",
            "order_payments",
        ]
