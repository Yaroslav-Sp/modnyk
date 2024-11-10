from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE

from common.models import BaseModel


class Cart(BaseModel):
    customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="carts")

    def __str__(self):
        return f"Cart №{self.pk} by {self.customer}"


class CartItem(BaseModel):
    cart = models.ForeignKey("cart.Cart", on_delete=CASCADE, related_name="cart_items")
    product = models.ForeignKey("products.Product", on_delete=CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f" {self.product} in cart {self.cart}"
