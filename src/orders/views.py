from django.shortcuts import render  # NOQA: 401
from django.views.generic import DetailView

from orders.models import Order


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        print(order.customer == self.request.user)
        if order.customer == self.request.user:
            context["order"] = order
        else:
            context["order"] = []
            context["error_message"] = "You do not have permission to view this order."
        return context
