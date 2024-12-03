from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE, SET_NULL, Avg, Count

from common.models import BaseModel
from reviews.models import Review


class CategoryLevel(models.IntegerChoices):
    GENDER_CLOTHES_TYPE = 0, "Gender clothes type"
    MAIN_CLOTHES_TYPE = 1, "Main clothes type"
    TYPE_CLOTHES = 2, "Type clothes"


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey("products.Category", on_delete=CASCADE, related_name="products")
    color = models.ForeignKey("products.Color", on_delete=CASCADE, related_name="products", null=True, blank=True)
    size = models.ManyToManyField("products.Size", related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey("products.Brand", on_delete=SET_NULL, null=True, related_name="products")

    def __str__(self):
        return f"№{self.pk} {self.name} - {self.category}"

    def average_rating(self):
        result = Review.objects.filter(product=self.pk).aggregate(Avg("rating"))
        return result["rating__avg"]

    def count_reviews(self):
        result = Review.objects.filter(product=self.pk).aggregate(Count("rating"))
        return result["rating__count"]

    def category_heritability(self):
        return f"{self.category.parent.parent.name} \u2B9E {self.category.parent.name} \u2B9E {self.category.name}"

    class Meta:
        ordering = ["-create_date"]


class Category(BaseModel):
    parent = models.ForeignKey(
        "products.Category", on_delete=models.CASCADE, blank=True, null=True, related_name="children"
    )
    name = models.CharField(max_length=255)
    level = models.SmallIntegerField(choices=CategoryLevel.choices, editable=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    @classmethod
    def get_history_for_categories(cls, categories, gender_name, main_category_name, sub_category_name):
        result = []

        for category in categories:
            grandparent_name = category.parent.parent.name if category.parent and category.parent.parent else None

            if gender_name:
                if grandparent_name in gender_name:
                    result.append(category)
            else:
                result.append(category)

        result2 = []
        for category in result:

            parent_name = category.parent.name if category.parent else None

            if main_category_name:
                if parent_name in main_category_name:
                    result2.append(category)
            else:
                result2.append(category)

        result3 = []
        for category in result2:

            current_name = category.name

            if sub_category_name:
                if current_name in sub_category_name:
                    result3.append(category)
            else:
                result3.append(category)

        return [item.id for item in result3]

    def __str__(self):
        if self.parent:
            return (
                f"Level {self.level} = {self.name}  -  [{self.parent.parent.name if self.parent.parent else None} -> "
                f"{self.parent.name if self.parent else None}]"
            )
        return self.name

    def clean(self):
        if self.level == 0 and self.parent:
            raise ValidationError("Main clothes type cannot have a parent category.")
        if self.level in (1, 2) and not self.parent:
            raise ValidationError("Type clothes must have a parent category.")
        super().clean()

    def get_children(self):
        return Category.objects.filter(parent=self)

    def get_descendant_categories(self):
        descendants = []

        def fetch_children(parent):
            children = Category.objects.filter(parent=parent)
            for child in children:
                descendants.append(child)
                fetch_children(child)

        fetch_children(self)
        return descendants


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
