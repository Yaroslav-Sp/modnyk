from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE

from common.models import BaseModel


class Cart(BaseModel):
    customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="carts")

    def total_cart_cost(self):
        return sum(item.total_item_cost() for item in self.cart_items.all())

    def __str__(self):
        return f"Cart №{self.pk} by {self.customer}"


class CartItem(BaseModel):
    cart = models.ForeignKey("cart.Cart", on_delete=CASCADE, related_name="cart_items")
    product = models.ForeignKey("products.Product", on_delete=CASCADE, related_name="cart_item")
    quantity = models.IntegerField()

    size = models.ForeignKey("products.Size", on_delete=CASCADE)

    def total_item_cost(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f" {self.product} in cart {self.cart}"
