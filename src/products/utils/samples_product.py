from decimal import Decimal

from products.models import (Brand, Category, CategoryLevel, Color, Product,
                             Size)


def sample_category():
    gender_category, _ = Category.objects.get_or_create(
        name="Men",
        level=CategoryLevel.GENDER_CLOTHES_TYPE,
    )
    main_category, _ = Category.objects.get_or_create(
        name="Outerwear",
        level=CategoryLevel.MAIN_CLOTHES_TYPE,
        parent=gender_category,
    )
    subcategory, _ = Category.objects.get_or_create(
        name="Shirts",
        level=CategoryLevel.TYPE_CLOTHES,
        parent=main_category,
    )
    return subcategory


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
