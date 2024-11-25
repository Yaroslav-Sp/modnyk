from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect, render  # NOQA: 401
from django.views.generic import DetailView

from accounts.forms import CustomerProfileForm
from accounts.models import Customer
from orders.forms import DeliveryAddressForm
from orders.models import Order
from reviews.models import Review


class CustomerProfile(DetailView):
    model = Customer
    template_name = "customer_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self.request.user, AnonymousUser):
            context["customers_reviews"] = []
            context["customer_orders"] = []
            context["customer_form"] = []
            context["delivery_address_form"] = []
        else:
            context["customers_reviews"] = Review.objects.filter(customer=self.request.user)
            context["customer_orders"] = Order.objects.filter(customer=self.request.user)
            context["customer_form"] = CustomerProfileForm(instance=self.request.user)
            context["delivery_address_form"] = DeliveryAddressForm(instance=self.request.user.customers_address.last())

        return context

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        post_request = request.POST
        if "change_customer_details" in post_request:
            form = CustomerProfileForm(post_request, request.FILES, instance=self.get_object())
            if form.is_valid():
                form.save()
                return redirect("customer:profile")
        elif "change_delivery_address" in post_request:
            form = DeliveryAddressForm(post_request, instance=self.request.user.customers_address.last())
            if form.is_valid():
                form.customer = self.request.user
                form.save()
                return redirect("customer:profile")
        return redirect("customer:profile")
