from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from products.models import Product
from reviews.forms import ReviewForm


class ProductInfo(DetailView, CreateView):
    model = Product
    form_class = ReviewForm
    template_name = "product_profile.html"
    context_object_name = "product"

    success_url = reverse_lazy("index")

    def form_valid(self, form):
        review = form.save(commit=False)
        review.customer = self.request.user
        review.save()
        return super().form_valid(form)



