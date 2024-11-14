from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.models import Product
from shop.models import PromotionBanner


class IndexView(ListView):
    model = Product
    template_name = "index.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banners"] = PromotionBanner.objects.all()
        return context


