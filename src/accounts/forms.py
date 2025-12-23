from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import Customer


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "phone_number", "email"]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "email": _("Email"),
        }

    @staticmethod
    def normalize_text(text) -> str:
        return text.strip().capitalize()

    def clean_first_name(self):
        return self.normalize_text(self.cleaned_data.get("first_name"))

    def clean_last_name(self):
        return self.normalize_text(self.cleaned_data.get("last_name"))


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email", "password1", "password2"]
