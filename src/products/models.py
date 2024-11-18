from django.db import models
from django.db.models import CASCADE, SET_NULL, Avg, Count

from common.models import BaseModel
from reviews.models import Review


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey("products.Category", on_delete=CASCADE, related_name="products")
    color = models.ForeignKey("products.Color", on_delete=CASCADE, related_name="products", null=True, blank=True)
    size = models.ManyToManyField("products.Size", related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey("products.Brand", on_delete=SET_NULL, null=True, related_name="products")

    def __str__(self):
        return f"({self.pk}) {self.name}"

    def average_rating(self):
        result = Review.objects.filter(product=self.pk).aggregate(Avg("rating"))
        return result["rating__avg"]

    def count_reviews(self):
        result = Review.objects.filter(product=self.pk).aggregate(Count("rating"))
        return result["rating__count"]

    class Meta:
        ordering = ["-create_date"]


class Category(BaseModel):
    parent_category = models.ForeignKey("products.Category", on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    category_level = models.SmallIntegerField(
        choices=[(0, "Gender/Age"), (1, "Type_clothes")],
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.parent_category} -> {self.name}"


class ProductImage(BaseModel):
    product = models.ForeignKey("products.Product", on_delete=CASCADE, related_name="products_images")
    image = models.ImageField(upload_to="img/products/products_images", null=True, blank=True)


class Size(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name}"


class Color(BaseModel):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="img/products/colors", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Brand(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
