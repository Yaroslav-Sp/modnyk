from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from orders.models import DeliveryAddress, DeliveryType, Order


class DeliveryAddressForm(forms.ModelForm):
    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer

    class Meta:
        model = DeliveryAddress
        fields = ["address_line_1", "address_line_2", "city", "state", "postal_code", "country"]
        widgets = {
            "address_line_1": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your address line 1"}
            ),
            "address_line_2": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your address line 2 (optional)"}
            ),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your city"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your state"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your postal code"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your country"}),
        }
        labels = {
            "address_line_1": _("Address line 1"),
            "address_line_2": _("Address line 2"),
            "city": _("City"),
            "state": _("State"),
            "postal_code": _("Postal code"),
            "country": _("Country"),
        }

    @staticmethod
    def normalize_text(text) -> str:
        return text.strip().capitalize()

    def clean(self):
        cleaned_data = super().clean()
        fields_to_normalize = self.fields

        for field in fields_to_normalize:
            value = cleaned_data.get(field)
            if value:
                cleaned_data[field] = self.normalize_text(value)

        return cleaned_data


class OrderForm(forms.ModelForm):
    recipients_phone_number = PhoneNumberField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your phone number"}),
    )

    class Meta:
        model = Order
        fields = [
            "recipients_first_name",
            "recipients_last_name",
            "recipients_phone_number",
        ]
        widgets = {
            "recipients_first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your first name"}
            ),
            "recipients_last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your last name"}
            ),
        }


class DeliveryTypeSelectForm(forms.Form):
    delivery_type = forms.ModelChoiceField(
        queryset=DeliveryType.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-control", "onchange": "this.form.submit();"}),
        initial=lambda: DeliveryType.objects.first(),
    )
