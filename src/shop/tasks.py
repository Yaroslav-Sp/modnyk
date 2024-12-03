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
    sample_category_gender_level = ["Men", "Women", "Children"]
    sample_category_main_level = ["Outerwear", "Underwear", "Footwear", "Accessories", "Activewear", "Swimwear"]
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
        "Sleepwear",
        "Jeans",
    ]

    default_sizes = {
        "XS": "Extra Small",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "XL": "Extra Large",
    }

    for _ in range(count):
        gender_name = random.choice(sample_category_gender_level)
        main_category_name = random.choice(sample_category_main_level)
        type_name = random.choice(sample_category_type_level)

        gender_category, _ = Category.objects.get_or_create(
            name=gender_name,
            level=0,
        )
        main_category, _ = Category.objects.get_or_create(
            name=main_category_name,
            level=1,
            parent=gender_category,
        )
        subcategory, _ = Category.objects.get_or_create(
            name=type_name,
            level=2,
            parent=main_category,
        )

        brand_name = fake.word(part_of_speech="noun").capitalize()
        brand, _ = Brand.objects.get_or_create(name=brand_name)

        random_size = random.choice(list(default_sizes.keys()))
        size_name = random_size
        size_description = default_sizes[random_size]
        size, _ = Size.objects.get_or_create(
            name=size_name,
            description=size_description,
        )

        color_name = fake.color_name()
        color, _ = Color.objects.get_or_create(name=color_name)

        product_data = {
            "name": fake.text(max_nb_chars=30),
            "description": fake.text(max_nb_chars=500),
            "color": color,
            "price": Decimal(str(round(random.uniform(0.5, 500.0), 2))),
            "brand": brand,
            "category": subcategory,
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
