from django.http import HttpResponseRedirect

from shop.models import Favorite


class FavoriteMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            return self.handle_post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def handle_post(self, request, *args, **kwargs):
        product_id = request.POST.get("favorite_form")
        general_params = {"customer": request.user, "product_id": product_id}
        favorite_item = Favorite.objects.filter(**general_params)

        if favorite_item.exists():
            favorite_item.delete()
        else:
            Favorite.objects.create(**general_params)

        return HttpResponseRedirect(request.path)
