from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from cart.models import Cart
from cart.utils.samples import sample_cart_item


class TestCart(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = get_user_model()(email="customer@example.com")
        self.user.set_password("12345678")

        self.user.save()
        self.test_cart = Cart.objects.create(customer=self.user)
        self.cart_items_count = 5

        for _ in range(1, self.cart_items_count + 1):
            sample_cart_item(cart=self.test_cart)

    def test_cart_creation(self):
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(self.test_cart.cart_items.count(), self.cart_items_count)

    def test_cart_total_quantity(self):
        total_quantity = sum(item.quantity for item in self.test_cart.cart_items.all())
        self.assertEqual(total_quantity, self.cart_items_count * sample_cart_item(cart=self.test_cart).quantity)
