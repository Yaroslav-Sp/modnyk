from django.contrib.auth import get_user_model
from django.db import models

from common.models import BaseModel


class Review(BaseModel):
    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="reviews")
    customer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="reviews")
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, max_length=3000)

    def __str__(self):
        return f"Review for {self.product} by {self.customer}"
