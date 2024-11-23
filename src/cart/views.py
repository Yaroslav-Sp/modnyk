from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.views.generic import ListView

from cart.models import Cart, CartItem


class CartView(ListView):
    model = CartItem
    template_name = "cart.html"
    context_object_name = "cart"

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Cart.objects.none()
        else:
            return CartItem.objects.filter(cart__customer=self.request.user)

    def post(self, request, *args, **kwargs):
        post_request = request.POST
        if "item_delete" in post_request:
            cart_item_id = post_request.get("item_delete")
            cart_item = CartItem.objects.filter(id=cart_item_id, cart__customer=self.request.user)
            cart_item.delete()
        elif "quantity-1" in post_request:
            cart_item_id = post_request.get("quantity-1")
            cart_item = CartItem.objects.filter(id=cart_item_id, cart__customer=self.request.user).first()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        elif "quantity+1" in post_request:
            cart_item_id = post_request.get("quantity+1")
            cart_item = CartItem.objects.filter(id=cart_item_id, cart__customer=self.request.user).first()
            if cart_item.quantity < 10:
                cart_item.quantity += 1
                cart_item.save()

        return redirect("cart:cart")
