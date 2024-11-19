from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, SET_NULL
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel


class Order(BaseModel):
    customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="customer_orders")
    status = models.SmallIntegerField(
        choices=[
            (0, "Pending"),
            (1, "Open"),
            (2, "Shipping"),
            (3, "Shipped"),
            (4, "Delivered"),
            (5, "Canceled"),
            (6, "Returned"),
        ],
        null=True,
        blank=True,
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.ForeignKey(
        "orders.DeliveryAddress", on_delete=SET_NULL, null=True, related_name="orders_addresses"
    )

    recipients_first_name = models.CharField(max_length=150, blank=True)
    recipients_last_name = models.CharField(max_length=150, blank=True)
    recipients_phone_number = PhoneNumberField()

    delivery_type = models.SmallIntegerField(
        choices=[(0, "Self-pickup"), (1, "Courier delivery"), (2, "Shipping"), (3, "Postal delivery")],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Order № {self.pk} by {self.customer}"


class OrderItem(BaseModel):
    order = models.ForeignKey("orders.Order", on_delete=SET_NULL, null=True, related_name="order_items")
    product = models.ForeignKey("products.Product", on_delete=CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f" Item {self.pk} {self.product} in order {self.order}"


class DeliveryAddress(BaseModel):
    customer = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, related_name="customers_address"
    )
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Delivery address"
        verbose_name_plural = "Delivery addresses"

    def __str__(self):
        return f" {self.country}, {self.state}, {self.city}, {self.street_address}, {self.postal_code}"


class Payment(BaseModel):
    order = models.ForeignKey("orders.Order", on_delete=SET_NULL, null=True, related_name="order_payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.SmallIntegerField(choices=[(0, "By cash"), (1, "By card")], null=True, blank=True)
    status = models.SmallIntegerField(choices=[(0, "Pending"), (1, "Cancelled"), (2, "Payed")], null=True, blank=True)

    def __str__(self):
        return f" Payment for order {self.order}"
