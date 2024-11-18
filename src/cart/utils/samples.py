from decimal import Decimal

from cart.models import CartItem
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
    product.size.set([size])

    default = {"product": product, "quantity": 2, "size": size}
    default.update(params)

    return CartItem.objects.create(cart=cart, **default)
