from django.db import models
from django.db.models import CASCADE, SET_NULL

from common.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey("products.Category", on_delete=CASCADE, related_name="products")
    size = models.ForeignKey("products.Size", on_delete=SET_NULL, null=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey("products.Brand", on_delete=SET_NULL, null=True, related_name="products")

    def __str__(self):
        return f"({self.pk}) {self.name}"


class Category(BaseModel):
    parent_category = models.ForeignKey("products.Category", on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)

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


class Brand(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
