import random
from decimal import Decimal

from celery import shared_task
from faker import Faker

from accounts.models import Customer
from products.models import Brand, Category, Color, Product, Size
from reviews.models import Review

fake = Faker()


@shared_task()
def create_product(count):
    sample_category_base_level = ["Men", "Women", "Children"]
    sample_category_type_level = [
        "Shirts",
        "Pants",
        "Dresses",
        "T-Shirts",
        "Shorts",
        "Jackets",
        "Sweaters",
        "Coats",
        "Suits",
        "Skirts",
        "Underwear",
        "Activewear",
        "Sleepwear",
        "Jeans",
        "Accessories",
    ]

    base_categories = [
        Category.objects.get_or_create(name=base_name, category_level=0)[0] for base_name in sample_category_base_level
    ]

    for base_category in base_categories:
        for type_name in sample_category_type_level:
            Category.objects.get_or_create(
                name=f"{base_category.name} {type_name}", category_level=1, parent_category=base_category
            )

    subcategories = list(Category.objects.filter(category_level=1))

    default_sizes = {
        "XS": "Extra Small",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "XL": "Extra Large",
    }

    for _ in range(count):
        category = random.choice(subcategories)

        brand, _ = Brand.objects.get_or_create(name=fake.word(part_of_speech="noun").capitalize())

        random_size = random.choice(list(default_sizes.keys()))
        size, _ = Size.objects.get_or_create(name=random_size, description=default_sizes[random_size])

        color, _ = Color.objects.get_or_create(name=fake.color_name())

        product_data = {
            "name": fake.text(max_nb_chars=30),
            "description": fake.text(max_nb_chars=500),
            "color": color,
            "price": Decimal(str(round(random.uniform(0.5, 500.0), 2))),
            "brand": brand,
            "category": category,
        }
        product = Product.objects.create(**product_data)
        product.size.set([size])
        product.save()


@shared_task()
def create_review(count):
    for _ in range(count):
        product = Product.objects.order_by("?").first()
        customer = Customer.objects.order_by("?").first()
        rating = random.randint(1, 5)
        comment = fake.text(max_nb_chars=500)

        review_data = {
            "product": product,
            "customer": customer,
            "rating": rating,
            "comment": comment,
        }
        Review.objects.create(**review_data)


@shared_task()
def sample_review(count):
    for _ in range(count):
        review_data = {
            "product": Product.objects.order_by("?").first(),
            "customer": Customer.objects.order_by("?").first(),
            "rating": random.randint(1, 5),
            "comment": fake.text(max_nb_chars=500),
        }
        Review.objects.create(**review_data)


@shared_task()
def create_customer(count):
    for _ in range(count):
        customer_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(domain="modnyk.net"),
            "is_staff": False,
            "is_active": True,
        }
        Customer.objects.create(**customer_data)
