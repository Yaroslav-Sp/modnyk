from decimal import Decimal

from products.models import Brand, Category, Color, Product, Size


def sample_category():
    default = {
        "name": "TestCategory",
        "category_level": "1",
    }
    return Category.objects.create(**default)


def sample_product(category):
    brand, _ = Brand.objects.get_or_create(name="TestBrand")
    size, _ = Size.objects.get_or_create(name="M", description="Medium size")
    color, _ = Color.objects.get_or_create(name="Red")

    default_product_data = {
        "name": "TestProduct",
        "description": "This is a test product description.",
        "color": color,
        "price": Decimal("9.99"),
        "brand": brand,
    }
    product = Product.objects.create(category=category, **default_product_data)
    product.size.set([size])

    return product
