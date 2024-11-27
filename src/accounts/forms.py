from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import Customer


class CustomerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        super(CustomerProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, customer=None):
        instance = super().save(commit=False)
        if customer:
            instance.user = customer
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email"]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "emai": _("Email"),
        }
