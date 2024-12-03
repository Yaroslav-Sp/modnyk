from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import DetailView

from cart.forms import CartItemForm
from cart.models import Cart, CartItem
from products.models import Product
from reviews.forms import ReviewForm
from shop.models import Favorite


class ProductInfo(DetailView):
    model = Product
    template_name = "product_profile.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reviews = self.object.reviews.all().order_by("-create_date")
        paginator = Paginator(reviews, 18)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["reviews"] = page_obj
        context["similar_products"] = Product.objects.all()
        context["review_form"] = ReviewForm()
        context["cart_form"] = CartItemForm()
        if isinstance(self.request.user, AnonymousUser):
            context["is_product_in_cart"] = []
            context["favorite_boolean"] = []
        else:
            context["favorite_boolean"] = Favorite.objects.filter(customer=self.request.user, product=self.get_object())
            context["is_product_in_cart"] = CartItem.objects.filter(
                cart__customer=self.request.user, product=self.get_object()
            ).first()
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        post_request = request.POST
        form_type = post_request.get("form_type")
        general_params = {"customer": self.request.user, "product": self.get_object()}

        if form_type == "review_form":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.customer = general_params["customer"]
                review.product = general_params["product"]
                review.save()

        elif form_type == "cart_form":
            form = CartItemForm(request.POST)
            if form.is_valid():
                cart_item = form.save(commit=False)
                cart, created = Cart.objects.get_or_create(customer=general_params["customer"])
                cart_item.cart = cart
                cart_item.product = general_params["product"]
                cart_item.save()

        elif form_type == "favorite_form":
            favorite_item = Favorite.objects.filter(**general_params)
            if favorite_item.exists():
                favorite_item.delete()
            else:
                Favorite.objects.create(**general_params)

        return redirect("products:product_info", pk=product.pk)
