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
    recipients_first_name = models.CharField(max_length=150, blank=True)
    recipients_last_name = models.CharField(max_length=150, blank=True)
    recipients_phone_number = PhoneNumberField()
    delivery_address = models.ForeignKey(
        "orders.DeliveryAddress", on_delete=SET_NULL, null=True, related_name="orders_addresses"
    )
    delivery_type = models.ForeignKey("orders.DeliveryType", on_delete=models.CASCADE, null=True, blank=True)
    cost_of_delivery = models.DecimalField(max_digits=10, decimal_places=2)

    def get_recipients_full_name(self):
        return f"{self.recipients_first_name} {self.recipients_last_name}"

    def __str__(self):
        return f"Order № {self.pk} by {self.customer}"

    def total_order_items_cost(self):
        return sum(item.total_item_cost() for item in self.order_items.all())

    def total_order_amount(self):
        return self.cost_of_delivery + self.total_order_items_cost()


class OrderItem(BaseModel):
    order = models.ForeignKey("orders.Order", on_delete=SET_NULL, null=True, related_name="order_items")
    product = models.ForeignKey("products.Product", on_delete=CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_item_cost(self):
        return self.quantity * self.price

    def __str__(self):
        return f" Item {self.pk} {self.product} in order {self.order}"


class DeliveryAddress(BaseModel):
    customer = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, related_name="customers_address"
    )
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Delivery address"
        verbose_name_plural = "Delivery addresses"

    def __str__(self):
        return (
            f" {self.address_line_1}, {self.address_line_2}, {self.city}, {self.state}, {self.postal_code}, "
            f"{self.country}"
        )


class Payment(BaseModel):
    order = models.ForeignKey("orders.Order", on_delete=SET_NULL, null=True, related_name="order_payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.SmallIntegerField(choices=[(0, "By cash"), (1, "By card")], null=True, blank=True)
    status = models.SmallIntegerField(choices=[(0, "Pending"), (1, "Cancelled"), (2, "Payed")], null=True, blank=True)

    def __str__(self):
        return f" Payment for order {self.order}"


class DeliveryType(models.Model):
    name = models.CharField(max_length=255)
    default_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
