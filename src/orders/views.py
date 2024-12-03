from django.shortcuts import get_object_or_404, redirect, render  # NOQA: 401
from django.views import View
from django.views.generic import DetailView

from cart.models import Cart, CartItem
from orders.forms import DeliveryAddressForm, DeliveryTypeSelectForm, OrderForm
from orders.models import DeliveryAddress, DeliveryType, Order, OrderItem


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_details.html"

    def get_queryset(self):
        return super().get_queryset().select_related("customer", "delivery_address").prefetch_related("order_items")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        if order.customer == self.request.user:
            context["order"] = order
        else:
            context["order"] = []
            context["error_message"] = "You do not have permission to view this order."
        return context


class OrderCheckoutView(View):
    def get_context_data(self, **kwargs):
        default_user_data = self.request.user
        cart = Cart.objects.prefetch_related("cart_items__product").get(customer=default_user_data)
        delivery_type_form = kwargs.get("delivery_type_form", DeliveryTypeSelectForm())
        delivery_cost = kwargs.get("delivery_cost", 0)

        last_address = DeliveryAddress.objects.filter(customer=self.request.user).last()

        context = {
            "order_form": kwargs.get(
                "order_form",
                OrderForm(
                    initial={
                        "recipients_first_name": default_user_data.first_name,
                        "recipients_last_name": default_user_data.last_name,
                        "recipients_phone_number": default_user_data.phone_number,
                    }
                ),
            ),
            "address_form": kwargs.get("address_form", DeliveryAddressForm(instance=last_address)),
            "delivery_type_form": delivery_type_form,
            "cart": cart,
            "delivery_cost": delivery_cost,
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, "order_checkout.html", context)

    def post(self, request):
        cart = Cart.objects.get(customer=self.request.user)
        delivery_type_form = DeliveryTypeSelectForm(request.POST)
        address_form = DeliveryAddressForm(request.POST)
        order_form = OrderForm(request.POST)

        if "delivery_type" in request.POST and "create_order" not in request.POST:
            if delivery_type_form.is_valid():
                delivery_type = delivery_type_form.cleaned_data["delivery_type"]
                delivery_cost = delivery_type.default_cost

                context = self.get_context_data(
                    delivery_type_form=delivery_type_form,
                    delivery_cost=delivery_cost,
                    address_form=address_form,
                    order_form=order_form,
                )
                return render(request, "order_checkout.html", context)

        order_form = OrderForm(request.POST)
        address_form = DeliveryAddressForm(request.POST)

        if order_form.is_valid() and address_form.is_valid():

            delivery_address = address_form.save(commit=False)
            delivery_address.customer = request.user
            delivery_address.save()

            order = order_form.save(commit=False)
            order.customer = request.user
            order.delivery_address = delivery_address
            delivery_type = DeliveryType.objects.get(pk=request.POST.get("delivery_type"))
            delivery_cost = delivery_type.default_cost
            order.delivery_type = delivery_type
            order.cost_of_delivery = 0 if cart.total_cart_cost() > 50 else delivery_cost
            order.status = 1
            order.save()

            cart_items = cart.cart_items.all()
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order, product=cart_item.product, quantity=cart_item.quantity, price=cart_item.product.price
                )
            CartItem.objects.filter(cart__customer=request.user).delete()

            return redirect("orders:detail", pk=order.pk)

        context = self.get_context_data(order_form=order_form, address_form=address_form)
        return render(request, "order_checkout.html", context)
