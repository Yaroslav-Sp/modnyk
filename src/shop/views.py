from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import ListView

from products.models import Product
from shop.models import Favorite, PromotionBanner


class IndexView(ListView):
    model = Product
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(Product.objects.all(), 50)
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

    def post(self, request, *args, **kwargs):
        post_request = request.POST
        product_id = post_request.get("product")
        product = Product.objects.get(id=product_id)

        general_params = {"customer": self.request.user, "product": product}

        favorite_item = Favorite.objects.filter(**general_params)
        if favorite_item.exists():
            favorite_item.delete()
        else:
            Favorite.objects.create(**general_params)

        return redirect("shop:index")


class FavouritesView(ListView):
    model = Favorite
    template_name = "wishlist.html"
    context_object_name = "favorites"

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Favorite.objects.none()
        else:
            return Favorite.objects.filter(customer=self.request.user)

    def post(self, request, *args, **kwargs):
        post_request = request.POST
        product_id = post_request.get("product_delete")
        product = Product.objects.get(id=product_id)

        general_params = {"customer": self.request.user, "product": product}

        favorite_item = Favorite.objects.filter(**general_params)
        if favorite_item.exists():
            favorite_item.delete()

        return redirect("shop:favorites_list")
