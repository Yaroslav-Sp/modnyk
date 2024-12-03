from decimal import Decimal

from cart.models import CartItem
from products.models import Brand, Category, Color, Product, Size


def sample_cart_item(cart, **params):
    sample_category_gender_level = "Men"
    sample_category_main_level = "Outerwear"
    sample_category_type_level = "Shirts"

    gender_category, _ = Category.objects.get_or_create(
        name=sample_category_gender_level,
        level=0,
    )
    main_category, _ = Category.objects.get_or_create(
        name=sample_category_main_level,
        level=1,
        parent=gender_category,
    )
    subcategory, _ = Category.objects.get_or_create(
        name=sample_category_type_level,
        level=2,
        parent=main_category,
    )

    category = subcategory
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
