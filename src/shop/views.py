from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from common.views import FavoriteMixin
from products.models import Product
from shop.models import Favorite, PromotionBanner
from shop.tasks import create_customer, create_product, create_review


class IndexView(FavoriteMixin, ListView):
    model = Product
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(
            Product.objects.prefetch_related("products_images", "reviews")
            .annotate(average_rating=Avg("reviews__rating"), review_count=Count("reviews"))
            .order_by("create_date"),
            48,
        )
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["products"] = page_obj
        context["banners"] = PromotionBanner.objects.all()
        if isinstance(self.request.user, AnonymousUser):
            context["favorite_boolean"] = []
        else:
            context["favorite_boolean"] = Favorite.objects.filter(customer=self.request.user).values_list(
                "product", flat=True
            )
        return context


class FavouritesView(LoginRequiredMixin, FavoriteMixin, ListView):
    template_name = "wishlist.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return (
            Product.objects.filter(favorites__customer=self.request.user)
            .prefetch_related("products_images")
            .annotate(average_rating=Avg("reviews__rating"), review_count=Count("reviews"))
        )


# celery_views


def product_generator(request: HttpRequest) -> HttpResponse:
    create_product(5)
    return HttpResponse("Task is started")


def reviews_generator(request: HttpRequest) -> HttpResponse:
    create_review(10)
    return HttpResponse("Task is started")


def customer_generator(request: HttpRequest) -> HttpResponse:
    create_customer(10)
    return HttpResponse("Task is started")
