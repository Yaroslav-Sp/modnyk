from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView

from cart.models import CartItem


class CartView(LoginRequiredMixin, ListView):
    template_name = "cart.html"
    context_object_name = "cart"

    def get_queryset(self):
        return (
            CartItem.objects.filter(cart__customer=self.request.user)
            .select_related("cart__customer", "product")
            .prefetch_related("product__color", "product__products_images")
        )

    def post(self, request, *args, **kwargs):
        post_request = request.POST
        if "item_delete" in post_request:
            cart_item_id = post_request.get("item_delete")
            cart_item = CartItem.objects.get(id=cart_item_id, cart__customer=self.request.user)
            cart_item.delete()
        elif "quantity-1" in post_request:
            cart_item_id = post_request.get("quantity-1")
            cart_item = CartItem.objects.get(id=cart_item_id, cart__customer=self.request.user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        elif "quantity+1" in post_request:
            cart_item_id = post_request.get("quantity+1")
            cart_item = CartItem.objects.get(id=cart_item_id, cart__customer=self.request.user)
            if cart_item.quantity < 10:
                cart_item.quantity += 1
                cart_item.save()

        return redirect("cart:cart")
