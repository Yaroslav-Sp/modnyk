from decimal import Decimal

from django.contrib.auth import get_user_model

from cart.models import Cart, CartItem
from products.models import Brand, Category, Product, Size

# def sample_cart_item(cart: Cart, **params):
#     default = {"product": Product.objects.get_or_create(name="TestProduct")[0], "quantity": 2}
#     default.update(params)
#
#     return CartItem.objects.create(cart=cart, **default)


def sample_cart_item(cart, **params):
    category, _ = Category.objects.get_or_create(name="TestCategory")
    brand, _ = Brand.objects.get_or_create(name="TestBrand")
    size, _ = Size.objects.get_or_create(name="M", description="Medium size")

    default_product_data = {
        "name": "TestProduct",
        "description": "This is a test product description.",
        "category": category,
        "size": size,
        "price": Decimal("9.99"),  # Чітке значення з двома десятковими знаками
        "brand": brand,
    }

    # Створюємо або отримуємо продукт з повними параметрами
    product, _ = Product.objects.get_or_create(**default_product_data)

    # Оновлюємо параметри для CartItem
    default = {"product": product, "quantity": 2}
    default.update(params)

    return CartItem.objects.create(cart=cart, **default)
