from django import forms
from django.utils.translation import gettext_lazy as _

from orders.models import DeliveryAddress


class DeliveryAddressForm(forms.ModelForm):
    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.customer:
            instance.customer = self.customer
        if commit:
            instance.save()
        return instance

    class Meta:
        model = DeliveryAddress
        fields = ["address_line_1", "address_line_2", "city", "state", "postal_code", "country"]
        widgets = {
            "address_line_1": forms.TextInput(attrs={"placeholder": "Street Address"}),
            "address_line_2": forms.TextInput(attrs={"placeholder": "Apartment, Suite, etc."}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "state": forms.TextInput(attrs={"placeholder": "State"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "Postal Code"}),
            "country": forms.TextInput(attrs={"placeholder": "Country"}),
        }
        labels = {
            "address_line_1": _("Address line 1"),
            "address_line_2": _("Address line 2"),
            "city": _("City"),
            "state": _("State"),
            "postal_code": _("Postal code"),
            "country": _("Country"),
        }
