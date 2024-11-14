from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE

from common.models import BaseModel


class Favorite(BaseModel):
    customer = models.ForeignKey(get_user_model(), on_delete=CASCADE, related_name="favorites")
    product = models.ForeignKey("products.Product", on_delete=CASCADE, related_name="favorites")

    def __str__(self):
        return f" {self.product}"


class PromotionBanner(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    image = models.ImageField(upload_to="img/shop/promotion_banner", null=True, blank=True)
