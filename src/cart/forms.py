from django import forms
from django.utils.translation import gettext_lazy as _

from cart.models import CartItem


class CartItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        super(CartItemForm, self).__init__(*args, **kwargs)

        self.fields["quantity"].required = True
        self.fields["size"].required = True

    def save(self, commit=True, customer=None):
        instance = super().save(commit=False)
        if customer:
            instance.user = customer
        if commit:
            instance.save()
        return instance

    class Meta:
        model = CartItem
        fields = ["size", "quantity"]
        widgets = {
            "quantity": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }
        labels = {
            "size": _("Select Size"),
            "quantity": _("Quantity"),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if not 1 <= quantity <= 10:
            raise forms.ValidationError(_("Quantity must be between 1 and 10."))
        return quantity
