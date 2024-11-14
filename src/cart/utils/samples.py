from decimal import Decimal

from django.contrib.auth import get_user_model

from cart.models import Cart, CartItem
from products.models import Brand, Category, Color, Product, Size


def sample_cart_item(cart, **params):
    category, _ = Category.objects.get_or_create(name="TestCategory", category_level=1)
    brand, _ = Brand.objects.get_or_create(name="TestBrand")
    size, _ = Size.objects.get_or_create(name="M", description="Medium size")
    color, _ = Color.objects.get_or_create(name="Red")

    default_product_data = {
        "name": "TestProduct",
        "description": "This is a test product description.",
        "category": category,
        "color": color,
        "price": Decimal("9.99"),
        "brand": brand,
    }

    product, _ = Product.objects.get_or_create(**default_product_data)
    product.size.add(size)

    default = {"product": product, "quantity": 2}
    default.update(params)

    return CartItem.objects.create(cart=cart, **default)
