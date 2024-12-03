from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render  # NOQA: 401
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (CreateView, DetailView, RedirectView,
                                  TemplateView)

from accounts.forms import CustomerProfileForm, UserRegistrationForm
from accounts.models import Customer
from accounts.services.email import send_registration_email
from accounts.utils.token_generator import TokenGenerator
from orders.forms import DeliveryAddressForm


class CustomerProfile(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "customer_profile.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("order_items", "reviews", "customer_orders", "customers_address")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customers_reviews"] = self.object.reviews.all()
        context["customer_orders"] = self.object.customer_orders.all()
        context["customer_form"] = CustomerProfileForm(instance=self.request.user)
        context["delivery_address_form"] = DeliveryAddressForm(instance=self.request.user.customers_address.last())
        return context

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post_request = request.POST
        context = self.get_context_data()

        if "change_customer_details" in post_request:
            customer_form = CustomerProfileForm(post_request, request, instance=self.get_object())
            if customer_form.is_valid():
                customer_form.save()
                return redirect("customer:profile")
            else:
                context["customer_form"] = customer_form
                return self.render_to_response(context)

        elif "change_delivery_address" in post_request:
            delivery_address_form = DeliveryAddressForm(
                post_request, instance=self.request.user.customers_address.last()
            )

            if delivery_address_form.is_valid():
                delivery_address = delivery_address_form.save(commit=False)
                delivery_address.customer = self.request.user
                delivery_address.save()
                return redirect("customer:profile")
            else:
                context["delivery_address_form"] = delivery_address_form
                return self.render_to_response(context)

        return redirect("customer:profile")


class UserLogin(LoginView):
    next_page = reverse_lazy("shop:index")


class UserLogout(LogoutView):
    next_page = reverse_lazy("shop:index")

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get":
            request.method = "POST"
        return super().dispatch(request, *args, **kwargs)


class UserRegistration(CreateView):
    template_name = "registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("registration_info")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(user_instance=self.object, request=self.request)
        return super().form_valid(form)


class UserActivationView(RedirectView):
    next_page = reverse_lazy("shop:index")

    def get(self, request, uuid64, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            return render(request, "registration/invalid_token.html")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()

            login(request, current_user)

            return super().get(request, *args, **kwargs)
        return render(request, "registration/invalid_token.html")


class InfoAfterRegistration(TemplateView):
    template_name = "registration/info_after_registration.html"
